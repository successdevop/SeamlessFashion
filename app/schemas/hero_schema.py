from app.models.hero_model import HeroBase


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass
