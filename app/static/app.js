let profileId = null;
let tripId = null;
let taskId = null;

const output = document.getElementById("output");
const qrBox = document.getElementById("qr-box");
const passToken = document.getElementById("pass-token");
const copyTokenBtn = document.getElementById("copy-token-btn");
const netStatus = document.getElementById("net-status");
const contextStatus = document.getElementById("context-status");
const currentViewLabel = document.getElementById("current-view-label");
const toastContainer = document.getElementById("toast-container");
const appViews = document.getElementById("app-views");
const cornerRibbon = document.querySelector(".corner-ribbon");
const featureWheel = document.getElementById("feature-wheel");
const featureWheelZone = document.querySelector(".semi-wheel-zone");
const featureOrbit = document.getElementById("feature-orbit");
const orbitItems = Array.from(document.querySelectorAll(".orbit-item[data-slot]"));

const profilesListWrap = document.getElementById("profiles-list-wrap");
const profilesList = document.getElementById("profiles-list");
const profilesListTip = document.getElementById("profiles-list-tip");
const refreshProfilesBtn = document.getElementById("refresh-profiles-btn");

const guideAnswer = document.getElementById("guide-answer");
const cardResult = document.getElementById("card-result");

const welcomeScreen = document.getElementById("welcome-screen");
const sliderTrack = document.getElementById("enter-slider-track");
const sliderThumb = document.getElementById("enter-slider-thumb");
const sliderProgress = document.getElementById("enter-slider-progress");
const sliderHint = document.getElementById("enter-slider-hint");

const queueKey = "anxingban_sos_queue";
let viewSwitchTimer = null;
let selectedFeatureIndex = 3;

const FEATURE_DEFS = [
  { label: "家庭建档", desc: "建立家庭成员档案", icon: "👤", view: "view-profile" },
  { label: "创建行程", desc: "定制专属旅行计划", icon: "📅", view: "view-trip" },
  { label: "紧急求助", desc: "一键联系紧急救助", icon: "SOS", view: "view-sos" },
  { label: "亲子任务", desc: "亲子互动趣味任务", icon: "👥", view: "view-task" },
  { label: "景点讲解", desc: "智能语音景点介绍", icon: "🎧", view: "view-guide" },
  { label: "回忆卡片", desc: "记录旅行美好瞬间", icon: "🖼", view: "view-card" },
];

function log(title, data) {
  if (!output) return;
  output.textContent = `[${new Date().toLocaleTimeString()}] ${title}\n${JSON.stringify(data, null, 2)}\n\n${output.textContent}`;
}

function showToast(message, type = "info", duration = 2400) {
  if (!toastContainer) return;
  const node = document.createElement("div");
  node.className = `toast ${type}`;
  node.textContent = message;
  toastContainer.appendChild(node);
  window.setTimeout(() => node.remove(), duration);
}

function updateNetStatus() {
  if (!netStatus) return;
  if (navigator.onLine) {
    netStatus.textContent = "网络状态：在线";
    netStatus.classList.add("online");
    netStatus.classList.remove("offline");
  } else {
    netStatus.textContent = "网络状态：离线";
    netStatus.classList.add("offline");
    netStatus.classList.remove("online");
  }
}

function updateContextStatus() {
  if (!contextStatus) return;
  contextStatus.textContent = `档案ID：${profileId ?? "-"} ｜ 行程ID：${tripId ?? "-"} ｜ 任务ID：${taskId ?? "-"}`;
}

function setBusy(button, busy, busyText = "处理中...") {
  if (!button) return;
  if (!button.dataset.idleText) {
    button.dataset.idleText = button.textContent;
  }
  button.disabled = busy;
  button.textContent = busy ? busyText : button.dataset.idleText;
}

function redrawRibbonHeart() {
  if (!cornerRibbon || !document.body.classList.contains("app-entered")) return;
  cornerRibbon.classList.remove("is-drawing");
  void cornerRibbon.offsetWidth;
  cornerRibbon.classList.add("is-drawing");
  window.setTimeout(() => {
    cornerRibbon.classList.remove("is-drawing");
  }, 1250);
}

function safeParseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

function syncFeatureSelector() {
  if (!orbitItems.length || !FEATURE_DEFS.length) return;
  if (selectedFeatureIndex < 0 || selectedFeatureIndex >= FEATURE_DEFS.length) {
    selectedFeatureIndex = 0;
  }

  const middleSlot = Math.floor(orbitItems.length / 2);
  orbitItems.forEach((slotNode, slotIndex) => {
    const relative = slotIndex - middleSlot;
    const featureIndex = (selectedFeatureIndex + relative + FEATURE_DEFS.length) % FEATURE_DEFS.length;
    const feature = FEATURE_DEFS[featureIndex];

    const titleNode = slotNode.querySelector(".orbit-title");
    const descNode = slotNode.querySelector(".orbit-desc");
    const iconNode = slotNode.querySelector(".orbit-icon");

    if (titleNode) titleNode.textContent = feature.label;
    if (descNode) descNode.textContent = feature.desc;
    if (iconNode) iconNode.textContent = feature.icon;
    slotNode.dataset.featureView = feature.view;
    slotNode.dataset.goView = feature.view;

    const isActive = slotIndex === middleSlot;
    slotNode.classList.toggle("active", isActive);
    slotNode.tabIndex = isActive ? 0 : -1;
    slotNode.setAttribute("aria-disabled", isActive ? "false" : "true");
  });
}

function rotateFeatureSelector(step) {
  if (!FEATURE_DEFS.length) return;
  const total = FEATURE_DEFS.length;
  selectedFeatureIndex = (selectedFeatureIndex + step + total) % total;
  syncFeatureSelector();
}

function enterSelectedFeature() {
  if (!FEATURE_DEFS.length) return;
  const targetView = FEATURE_DEFS[selectedFeatureIndex].view;
  if (!targetView) return;
  showView(targetView);
}

function initFeatureSelector() {
  if (!featureWheel || !featureWheelZone || !featureOrbit || !orbitItems.length) return;

  syncFeatureSelector();
  const middleSlot = Math.floor(orbitItems.length / 2);

  const activateOrbitItem = (item) => {
    if (!item) return;
    const target = item.dataset.featureView;
    const slot = Number(item.dataset.slot);
    if (!target || Number.isNaN(slot)) return;
    selectedFeatureIndex = (selectedFeatureIndex + slot - middleSlot + FEATURE_DEFS.length) % FEATURE_DEFS.length;
    syncFeatureSelector();
    showToast("正在打开功能页...", "info", 700);
    showView(target);
  };

  let dragging = false;
  let lastY = 0;
  let pointerStartX = 0;
  let pointerStartY = 0;
  let pointerStartItem = null;

  const onMove = (clientY) => {
    if (!dragging) return;
    const delta = clientY - lastY;
    if (Math.abs(delta) >= 26) {
      rotateFeatureSelector(delta > 0 ? 1 : -1);
      lastY = clientY;
    }
  };

  const handleWheelRotate = (event) => {
    event.preventDefault();
    if (Math.abs(event.deltaY) < 4) return;
    rotateFeatureSelector(event.deltaY > 0 ? 1 : -1);
  };

  const onPointerDown = (event) => {
    dragging = true;
    lastY = event.clientY;
    pointerStartX = event.clientX;
    pointerStartY = event.clientY;
    pointerStartItem = event.target.closest(".orbit-item[data-slot]");
    if (event.pointerId !== undefined && featureWheelZone.setPointerCapture) {
      featureWheelZone.setPointerCapture(event.pointerId);
    }
  };

  const onPointerMove = (event) => {
    onMove(event.clientY);
  };

  const onPointerEnd = (event) => {
    if (pointerStartItem) {
      const dx = Math.abs((event?.clientX ?? pointerStartX) - pointerStartX);
      const dy = Math.abs((event?.clientY ?? pointerStartY) - pointerStartY);
      if (dx < 12 && dy < 12) {
        activateOrbitItem(pointerStartItem);
      }
    }
    dragging = false;
    pointerStartItem = null;
  };

  const onMouseDown = (event) => {
    if (event.button !== 0) return;
    dragging = true;
    lastY = event.clientY;
  };

  const onMouseMove = (event) => {
    onMove(event.clientY);
  };

  const onMouseUp = () => {
    dragging = false;
  };

  const onTouchStart = (event) => {
    if (!event.touches?.[0]) return;
    dragging = true;
    lastY = event.touches[0].clientY;
    pointerStartX = event.touches[0].clientX;
    pointerStartY = event.touches[0].clientY;
    pointerStartItem = event.target.closest(".orbit-item[data-slot]");
  };

  const onTouchMove = (event) => {
    if (!event.touches?.[0]) return;
    onMove(event.touches[0].clientY);
  };

  const onTouchEnd = (event) => {
    if (pointerStartItem && event.changedTouches?.[0]) {
      const dx = Math.abs(event.changedTouches[0].clientX - pointerStartX);
      const dy = Math.abs(event.changedTouches[0].clientY - pointerStartY);
      if (dx < 12 && dy < 12) {
        activateOrbitItem(pointerStartItem);
      }
    }
    dragging = false;
    pointerStartItem = null;
  };

  featureWheel.addEventListener("wheel", handleWheelRotate, { passive: false });
  featureOrbit.addEventListener("wheel", handleWheelRotate, { passive: false });
  featureWheelZone.addEventListener("wheel", handleWheelRotate, { passive: false });

  featureWheel.addEventListener("pointerdown", onPointerDown);
  featureOrbit.addEventListener("pointerdown", onPointerDown);
  featureWheelZone.addEventListener("pointerdown", onPointerDown);

  featureWheel.addEventListener("pointermove", onPointerMove);
  featureOrbit.addEventListener("pointermove", onPointerMove);
  featureWheelZone.addEventListener("pointermove", onPointerMove);

  featureWheel.addEventListener("pointerup", onPointerEnd);
  featureOrbit.addEventListener("pointerup", onPointerEnd);
  featureWheelZone.addEventListener("pointerup", onPointerEnd);

  featureWheel.addEventListener("pointercancel", onPointerEnd);
  featureOrbit.addEventListener("pointercancel", onPointerEnd);
  featureWheelZone.addEventListener("pointercancel", onPointerEnd);

  featureWheelZone.addEventListener("mousedown", onMouseDown);
  featureOrbit.addEventListener("mousedown", onMouseDown);
  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);

  featureWheelZone.addEventListener("touchstart", onTouchStart, { passive: true });
  featureOrbit.addEventListener("touchstart", onTouchStart, { passive: true });
  featureWheelZone.addEventListener("touchmove", onTouchMove, { passive: true });
  featureOrbit.addEventListener("touchmove", onTouchMove, { passive: true });
  window.addEventListener("touchend", onTouchEnd);

  featureWheel.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowRight") {
      event.preventDefault();
      rotateFeatureSelector(1);
    } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
      event.preventDefault();
      rotateFeatureSelector(-1);
    } else if (event.key === "Enter") {
      event.preventDefault();
      enterSelectedFeature();
    }
  });

  orbitItems.forEach((item) => {
    item.addEventListener("click", () => {
      activateOrbitItem(item);
    });
    item.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activateOrbitItem(item);
      }
    });
  });

  featureOrbit.addEventListener("click", (event) => {
    const item = event.target.closest(".orbit-item[data-slot]");
    if (!item) return;
    activateOrbitItem(item);
  });

}

function getViewIds() {
  return Array.from(document.querySelectorAll(".view")).map((el) => el.id);
}

function updateCurrentViewLabel(viewId) {
  if (!currentViewLabel) return;
  const target = document.getElementById(viewId);
  currentViewLabel.textContent = target?.dataset.viewTitle || "首页 · 功能总览";
}

function syncViewTheme(viewId) {
  const isHome = viewId === "view-home";
  document.body.classList.toggle("view-home-active", isHome);
  document.body.classList.toggle("view-sub-active", !isHome);
}

function activateDock(viewId) {
  document.querySelectorAll(".dock-item[data-go-view]").forEach((item) => {
    item.classList.toggle("active", item.dataset.goView === viewId);
  });
}

function showView(viewId, options = {}) {
  const ids = getViewIds();
  const targetId = ids.includes(viewId) ? viewId : "view-home";
  const currentActiveId = document.querySelector(".view.active")?.id;
  const changedView = currentActiveId !== targetId;

  const applyView = () => {
    document.querySelectorAll(".view").forEach((view) => {
      view.classList.toggle("active", view.id === targetId);
    });

    if (appViews) {
      appViews.scrollTo({ top: 0, behavior: options.instant ? "auto" : "smooth" });
    }

    activateDock(targetId);
    updateCurrentViewLabel(targetId);
    syncViewTheme(targetId);
    if (changedView) {
      redrawRibbonHeart();
    }

    if (!options.fromHash) {
      const nextHash = targetId === "view-home" ? "" : `#${targetId}`;
      const nextUrl = `${window.location.pathname}${window.location.search}${nextHash}`;
      const nowUrl = `${window.location.pathname}${window.location.search}${window.location.hash}`;
      if (nextUrl !== nowUrl) {
        window.history.pushState(null, "", nextUrl);
      }
    }
  };

  if (!options.instant && currentActiveId && currentActiveId !== targetId && appViews) {
    appViews.classList.remove("view-switch-in");
    appViews.classList.add("view-switch-out");

    if (viewSwitchTimer) {
      window.clearTimeout(viewSwitchTimer);
    }

    viewSwitchTimer = window.setTimeout(() => {
      applyView();
      appViews.classList.remove("view-switch-out");
      appViews.classList.add("view-switch-in");
      window.setTimeout(() => {
        appViews.classList.remove("view-switch-in");
      }, 320);
    }, 140);
  } else {
    applyView();
  }
}

function resolveInitialView() {
  const hash = window.location.hash.replace("#", "").trim();
  return getViewIds().includes(hash) ? hash : "view-home";
}

function bindViewNavigation() {
  document.querySelectorAll("[data-go-view]").forEach((node) => {
    node.addEventListener("click", () => {
      if (!node.dataset.goView) return;
      showView(node.dataset.goView);
    });
  });

  window.addEventListener("hashchange", () => {
    showView(resolveInitialView(), { fromHash: true, instant: true });
  });
}

function getDockViewOrder() {
  return Array.from(document.querySelectorAll(".bottom-dock .dock-item[data-go-view]"))
    .map((item) => item.dataset.goView)
    .filter(Boolean);
}

function getAdjacentDockView(currentViewId, direction) {
  const order = getDockViewOrder();
  const currentIndex = order.indexOf(currentViewId);
  if (currentIndex < 0) return null;

  const targetIndex = direction === "next" ? currentIndex + 1 : currentIndex - 1;
  if (targetIndex < 0 || targetIndex >= order.length) return null;

  return order[targetIndex];
}

function initDockDragSwitch() {
  const dock = document.querySelector(".bottom-dock");
  if (!dock) return;

  let dragging = false;
  let startX = 0;
  let startY = 0;
  let moved = false;
  let suppressClickUntil = 0;

  const start = (clientX, clientY) => {
    dragging = true;
    moved = false;
    startX = clientX;
    startY = clientY;
  };

  const move = (clientX, clientY) => {
    if (!dragging) return;
    const dx = clientX - startX;
    const dy = clientY - startY;
    if (Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) {
      moved = true;
      dock.classList.add("is-dragging");
    }
  };

  const end = (clientX, clientY) => {
    if (!dragging) return;

    dragging = false;
    dock.classList.remove("is-dragging");

    const dx = clientX - startX;
    const dy = clientY - startY;

    if (!moved) return;
    suppressClickUntil = Date.now() + 220;

    if (Math.abs(dx) < 52 || Math.abs(dx) < Math.abs(dy) * 1.2) return;

    const currentViewId = document.querySelector(".view.active")?.id;
    const direction = dx < 0 ? "next" : "prev";
    const targetView = getAdjacentDockView(currentViewId, direction);
    if (!targetView) return;

    showView(targetView);
  };

  dock.addEventListener(
    "touchstart",
    (event) => {
      if (!event.touches?.[0]) return;
      const touch = event.touches[0];
      start(touch.clientX, touch.clientY);
    },
    { passive: true }
  );

  dock.addEventListener(
    "touchmove",
    (event) => {
      if (!event.touches?.[0]) return;
      const touch = event.touches[0];
      move(touch.clientX, touch.clientY);
    },
    { passive: true }
  );

  dock.addEventListener(
    "touchend",
    (event) => {
      if (!event.changedTouches?.[0]) return;
      const touch = event.changedTouches[0];
      end(touch.clientX, touch.clientY);
    },
    { passive: true }
  );

  dock.addEventListener("mousedown", (event) => {
    if (event.button !== 0) return;
    start(event.clientX, event.clientY);
  });

  window.addEventListener("mousemove", (event) => {
    move(event.clientX, event.clientY);
  });

  window.addEventListener("mouseup", (event) => {
    end(event.clientX, event.clientY);
  });

  dock.addEventListener(
    "click",
    (event) => {
      if (Date.now() < suppressClickUntil) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
    true
  );
}

function enableBrowserPreviewMode() {
  const isStandalone =
    window.matchMedia("(display-mode: standalone)").matches ||
    window.matchMedia("(display-mode: fullscreen)").matches ||
    window.navigator.standalone === true;

  if (!isStandalone) {
    document.body.classList.add("browser-preview");
  }
}

function initWelcomeEntry() {
  if (!welcomeScreen || !sliderTrack || !sliderThumb || !sliderProgress || !sliderHint) {
    document.body.classList.add("app-entered");
    redrawRibbonHeart();
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const skipWelcome = params.get("skipWelcome") === "1";

  if (skipWelcome) {
    document.body.classList.add("app-entered");
    redrawRibbonHeart();
    welcomeScreen.remove();
    return;
  }

  document.body.classList.remove("app-entered");

  let dragging = false;
  let unlocked = false;
  let startX = 0;
  let startOffset = 0;
  let currentOffset = 0;
  let maxOffset = 0;

  const updateSlider = (offset) => {
    currentOffset = Math.max(0, Math.min(offset, maxOffset));
    sliderThumb.style.transform = `translateX(${currentOffset}px)`;

    const ratio = maxOffset > 0 ? currentOffset / maxOffset : 0;
    sliderProgress.style.width = `${56 + ratio * (sliderTrack.clientWidth - 56)}px`;
    sliderHint.style.opacity = String(Math.max(0.12, 1 - ratio * 1.15));
  };

  const syncBounds = () => {
    maxOffset = Math.max(0, sliderTrack.clientWidth - sliderThumb.offsetWidth - 8);
    updateSlider(currentOffset);
  };

  const resetSlider = () => {
    sliderThumb.style.transition = "transform 220ms ease";
    sliderProgress.style.transition = "width 220ms ease";
    updateSlider(0);
    window.setTimeout(() => {
      sliderThumb.style.transition = "";
      sliderProgress.style.transition = "";
    }, 230);
  };

  const unlockApp = () => {
    if (unlocked) return;
    unlocked = true;
    sliderHint.textContent = "欢迎回来";
    document.body.classList.add("app-entered");
    redrawRibbonHeart();
    window.setTimeout(() => {
      welcomeScreen.remove();
      showToast("欢迎进入安行伴", "success", 1800);
    }, 360);
  };

  const startDrag = (clientX) => {
    if (unlocked) return;
    dragging = true;
    startX = clientX;
    startOffset = currentOffset;
  };

  const moveDrag = (clientX) => {
    if (!dragging || unlocked) return;
    updateSlider(startOffset + (clientX - startX));
  };

  const endDrag = () => {
    if (!dragging || unlocked) return;
    dragging = false;
    const ratio = maxOffset > 0 ? currentOffset / maxOffset : 0;
    if (ratio >= 0.88) {
      updateSlider(maxOffset);
      unlockApp();
    } else {
      resetSlider();
    }
  };

  sliderThumb.addEventListener("pointerdown", (event) => {
    startDrag(event.clientX);
    sliderThumb.setPointerCapture(event.pointerId);
  });
  sliderThumb.addEventListener("pointermove", (event) => moveDrag(event.clientX));
  sliderThumb.addEventListener("pointerup", endDrag);
  sliderThumb.addEventListener("pointercancel", endDrag);

  sliderThumb.addEventListener("mousedown", (event) => startDrag(event.clientX));
  window.addEventListener("mousemove", (event) => moveDrag(event.clientX));
  window.addEventListener("mouseup", endDrag);

  sliderThumb.addEventListener(
    "touchstart",
    (event) => {
      if (event.touches?.[0]) {
        startDrag(event.touches[0].clientX);
      }
    },
    { passive: true }
  );
  window.addEventListener(
    "touchmove",
    (event) => {
      if (event.touches?.[0]) {
        moveDrag(event.touches[0].clientX);
      }
    },
    { passive: true }
  );
  window.addEventListener("touchend", endDrag);

  sliderTrack.addEventListener("click", (event) => {
    if (dragging || unlocked) return;
    const rect = sliderTrack.getBoundingClientRect();
    const clickedRatio = (event.clientX - rect.left) / rect.width;
    if (clickedRatio > 0.9) {
      updateSlider(maxOffset);
      unlockApp();
    }
  });

  sliderHint.addEventListener("click", () => {
    if (unlocked) return;
    updateSlider(maxOffset);
    unlockApp();
  });

  sliderThumb.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      updateSlider(maxOffset);
      unlockApp();
    }
  });

  window.addEventListener("resize", syncBounds);
  syncBounds();
}

function validateForm(form) {
  const requiredInputs = form.querySelectorAll("input[required]");
  for (const input of requiredInputs) {
    if (!input.value.trim()) {
      showToast(`请先填写：${input.placeholder || input.name}`, "warn");
      input.focus();
      return false;
    }
  }
  return true;
}

async function api(path, method = "GET", body) {
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), 12000);

  const init = {
    method,
    headers: { "Content-Type": "application/json" },
    signal: controller.signal,
  };
  if (body) {
    init.body = JSON.stringify(body);
  }

  try {
    const res = await fetch(path, init);
    const raw = await res.text();

    let data = {};
    if (raw) {
      try {
        data = JSON.parse(raw);
      } catch {
        data = { detail: raw.slice(0, 120) };
      }
    }

    if (!res.ok) {
      throw new Error(data.detail || `请求失败 (${res.status})`);
    }

    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("请求超时，请稍后重试");
    }
    throw error;
  } finally {
    window.clearTimeout(timer);
  }
}

function getQueue() {
  try {
    return JSON.parse(localStorage.getItem(queueKey) || "[]");
  } catch {
    return [];
  }
}

function setQueue(items) {
  localStorage.setItem(queueKey, JSON.stringify(items));
}

async function flushSOSQueue() {
  const queue = getQueue();
  if (!queue.length) return;

  const rest = [];
  for (const item of queue) {
    try {
      const data = await api("/api/sos/trigger", "POST", { ...item, network_status: "restored" });
      log("离线求助已补发", data);
    } catch {
      rest.push(item);
    }
  }

  setQueue(rest);
  if (rest.length === 0) {
    showToast("离线求助已全部补发", "success");
  }
}

function renderProfiles(items) {
  if (!profilesListWrap || !profilesList || !profilesListTip) return;

  profilesListWrap.classList.remove("hidden");
  profilesList.innerHTML = "";

  if (!items || items.length === 0) {
    profilesListTip.textContent = "暂无已填写信息";
    return;
  }

  profilesListTip.textContent = `已填写 ${items.length} 条信息`;
  for (const item of items) {
    const health = safeParseJson(item.health_info || "{}");

    const li = document.createElement("li");
    const title = document.createElement("div");
    title.className = "title";
    title.textContent = `${item.parent_name}（子女：${item.child_name}）`;

    const contact = document.createElement("div");
    contact.className = "meta";
    contact.textContent = `父母手机号：${item.parent_phone} ｜ 子女手机号：${item.child_phone}`;

    const interests = document.createElement("div");
    interests.className = "meta";
    interests.textContent = `兴趣：${item.interests || "-"}`;

    const healthMeta = document.createElement("div");
    healthMeta.className = "meta";
    healthMeta.textContent = `慢性病：${health.chronic_diseases || "无"} ｜ 过敏史：${health.allergies || "无"}`;

    li.append(title, contact, interests, healthMeta);
    profilesList.appendChild(li);
  }
}

async function loadProfiles(limit = 20) {
  try {
    const items = await api(`/api/profiles?limit=${limit}`);
    renderProfiles(items);
  } catch (error) {
    if (profilesListWrap && profilesListTip) {
      profilesListWrap.classList.remove("hidden");
      profilesListTip.textContent = `读取失败：${error.message}`;
    }
    showToast(`信息读取失败：${error.message}`, "error");
  }
}

function bindFeatureEvents() {
  const profileForm = document.getElementById("profile-form");
  if (profileForm) {
    profileForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!validateForm(profileForm)) return;

      const submitBtn = profileForm.querySelector('button[type="submit"]');
      setBusy(submitBtn, true, "创建中...");
      try {
        const payload = Object.fromEntries(new FormData(profileForm).entries());
        const data = await api("/api/profiles", "POST", payload);
        profileId = data.id;
        updateContextStatus();
        await loadProfiles();
        log("档案创建成功", data);
        showToast("档案创建成功", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(submitBtn, false);
      }
    });
  }

  const tripForm = document.getElementById("trip-form");
  if (tripForm) {
    tripForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!validateForm(tripForm)) return;

      if (!profileId) {
        showToast("请先创建家庭档案", "warn");
        showView("view-profile");
        return;
      }

      const submitBtn = tripForm.querySelector('button[type="submit"]');
      setBusy(submitBtn, true, "创建中...");
      try {
        const payload = Object.fromEntries(new FormData(tripForm).entries());
        payload.profile_id = profileId;

        const data = await api("/api/trips", "POST", payload);
        tripId = data.id;
        updateContextStatus();

        if (qrBox) {
          qrBox.innerHTML = data.pass_qr_svg;
        }
        if (passToken) {
          passToken.classList.remove("hidden");
          passToken.textContent = `动态通行码：${data.pass_token}`;
        }
        if (copyTokenBtn) {
          copyTokenBtn.classList.remove("hidden");
        }

        log("行程创建成功", data);
        showToast("行程创建成功，已生成通行码", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(submitBtn, false);
      }
    });
  }

  if (copyTokenBtn && passToken) {
    copyTokenBtn.addEventListener("click", async () => {
      const text = passToken.textContent.replace("动态通行码：", "").trim();
      if (!text) {
        showToast("暂无可复制的通行码", "warn");
        return;
      }

      try {
        await navigator.clipboard.writeText(text);
        showToast("通行码已复制", "success");
      } catch {
        showToast("复制失败，请手动复制", "warn");
      }
    });
  }

  const sosBtn = document.getElementById("sos-btn");
  if (sosBtn) {
    sosBtn.addEventListener("click", async () => {
      if (!profileId) {
        showToast("请先创建家庭档案", "warn");
        showView("view-profile");
        return;
      }

      const payload = {
        profile_id: profileId,
        trip_id: tripId,
        latitude: 29.56301,
        longitude: 106.55156,
        network_status: navigator.onLine ? "online" : "offline",
      };

      setBusy(sosBtn, true, "发送中...");
      try {
        if (!navigator.onLine) throw new Error("offline");
        const data = await api("/api/sos/trigger", "POST", payload);
        log("求助已触发", data);
        showToast("求助已触发，已走双通道通知", "success");
      } catch {
        const queue = getQueue();
        queue.push(payload);
        setQueue(queue);
        log("求助已加入离线队列", { queued: queue.length });
        showToast(`离线状态下已排队，待发送 ${queue.length} 条`, "warn", 3200);
      } finally {
        setBusy(sosBtn, false);
      }
    });
  }

  const taskForm = document.getElementById("task-form");
  if (taskForm) {
    taskForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!validateForm(taskForm)) return;

      if (!profileId || !tripId) {
        showToast("请先创建档案和行程", "warn");
        showView(!profileId ? "view-profile" : "view-trip");
        return;
      }

      const submitBtn = taskForm.querySelector('button[type="submit"]');
      setBusy(submitBtn, true, "创建中...");
      try {
        const payload = Object.fromEntries(new FormData(taskForm).entries());
        payload.profile_id = profileId;
        payload.trip_id = tripId;

        const data = await api("/api/tasks", "POST", payload);
        taskId = data.id;
        updateContextStatus();
        log("任务创建成功", data);
        showToast("挑战任务已创建", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(submitBtn, false);
      }
    });
  }

  const completeBtn = document.getElementById("task-complete-btn");
  if (completeBtn) {
    completeBtn.addEventListener("click", async () => {
      if (!taskId) {
        showToast("请先创建任务", "warn");
        return;
      }

      setBusy(completeBtn, true, "提交中...");
      try {
        const data = await api(`/api/tasks/${taskId}/complete`, "POST", {
          completed_note: "已完成本次挑战",
          photo_url: "https://example.com/photo.jpg",
        });
        log("任务已完成", data);
        showToast("已标记任务完成", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(completeBtn, false);
      }
    });
  }

  const feedbackBtn = document.getElementById("task-feedback-btn");
  if (feedbackBtn) {
    feedbackBtn.addEventListener("click", async () => {
      if (!taskId) {
        showToast("请先创建任务", "warn");
        return;
      }

      setBusy(feedbackBtn, true, "发送中...");
      try {
        const data = await api(`/api/tasks/${taskId}/feedback`, "POST", {
          feedback_text: "太棒了，继续保持！",
          hearts_delta: 1,
        });
        log("反馈已发送", data);
        showToast("反馈成功，爱心+1", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(feedbackBtn, false);
      }
    });
  }

  const guideForm = document.getElementById("guide-form");
  if (guideForm) {
    guideForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!validateForm(guideForm)) return;

      const submitBtn = guideForm.querySelector('button[type="submit"]');
      setBusy(submitBtn, true, "查询中...");
      try {
        const payload = Object.fromEntries(new FormData(guideForm).entries());
        const data = await api("/api/guide/ask", "POST", payload);

        const answerText = data.answer || data.reply || data.detail || JSON.stringify(data, null, 2);
        if (guideAnswer) {
          guideAnswer.classList.remove("hidden");
          guideAnswer.textContent = `讲解结果：${answerText}`;
        }

        log("讲解回答", data);
        showToast("已返回讲解结果", "info");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(submitBtn, false);
      }
    });
  }

  const cardBtn = document.getElementById("card-btn");
  if (cardBtn) {
    cardBtn.addEventListener("click", async () => {
      if (!tripId) {
        showToast("请先创建行程", "warn");
        showView("view-trip");
        return;
      }

      setBusy(cardBtn, true, "生成中...");
      try {
        const data = await api("/api/cards/generate", "POST", {
          trip_id: tripId,
          title: "安行伴·重庆数字回忆卡",
          image_url: "",
        });

        if (cardResult) {
          cardResult.classList.remove("hidden");
          cardResult.textContent = `回忆卡已生成：${data.title || data.id || "已完成"}`;
        }

        log("回忆卡已生成", data);
        showToast("数字回忆卡已生成", "success");
      } catch (error) {
        showToast(error.message, "error");
      } finally {
        setBusy(cardBtn, false);
      }
    });
  }

  if (refreshProfilesBtn) {
    refreshProfilesBtn.addEventListener("click", async () => {
      setBusy(refreshProfilesBtn, true, "加载中...");
      await loadProfiles();
      setBusy(refreshProfilesBtn, false);
    });
  }

  document.querySelectorAll(".scenic-card[data-go-view][data-destination]").forEach((card) => {
    card.addEventListener("click", () => {
      const destination = card.dataset.destination?.trim();
      if (!destination) return;
      showToast(`已进入 ${destination} 景区介绍`, "info", 1600);
    });
  });

  document.querySelectorAll(".scenic-plan-btn[data-destination]").forEach((button) => {
    button.addEventListener("click", () => {
      const destination = button.dataset.destination?.trim();
      if (!destination) return;

      const destinationInput = document.querySelector('#trip-form input[name="destination"]');
      if (destinationInput) {
        destinationInput.value = destination;
      }

      showToast(`已将 ${destination} 加入行程，请继续创建行程`, "success", 2200);
    });
  });

  document.querySelectorAll(".scenic-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".scenic-tab").forEach((node) => {
        node.classList.remove("active");
      });
      tab.classList.add("active");
    });
  });
}

function boot() {
  const travelDateInput = document.querySelector('input[name="travel_date"]');
  if (travelDateInput) {
    travelDateInput.value = new Date().toISOString().slice(0, 10);
  }

  bindViewNavigation();
  initFeatureSelector();
  initDockDragSwitch();
  bindFeatureEvents();

  enableBrowserPreviewMode();
  updateNetStatus();
  updateContextStatus();

  showView(resolveInitialView(), { fromHash: true, instant: true });

  window.addEventListener("online", () => {
    updateNetStatus();
    flushSOSQueue();
  });
  window.addEventListener("offline", updateNetStatus);

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js").catch(() => {
      showToast("离线能力初始化失败", "warn");
    });
  }

  flushSOSQueue();
  initWelcomeEntry();
  showToast("应用已就绪，可从首页卡片进入功能页面", "info", 1800);
}

boot();
