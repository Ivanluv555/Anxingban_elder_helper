from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.card.dto.CardDto import CardGenerateDto, CardResponseDto
from app.modules.card.service.CardService import CardService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.post("/generate", response_model=CardResponseDto)
def generate_card(payload: CardGenerateDto, db: Session = Depends(get_db)):
    trip = TripService.get_trip_by_id(db, payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    card = CardService.generate_card(db, payload.trip_id, payload.title, payload.image_url, trip)
    return card


@router.get("/{card_id}", response_model=CardResponseDto)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/trip/{trip_id}", response_model=list[CardResponseDto])
def list_cards_by_trip(trip_id: int, db: Session = Depends(get_db)):
    return CardService.list_cards_by_trip(db, trip_id)
