from fastapi import APIRouter, Request
from pydantic import BaseModel

courses_router = APIRouter(prefix="/courses")


class CourseSchema(BaseModel):
    exchanger: str
    direction: str
    value: float


class CoursesResponse(BaseModel):
    courses: list[CourseSchema]


@courses_router.get("", response_model=CoursesResponse)
async def get_all_courses(request: Request) -> CoursesResponse:
    service = request.app.container.courses_service

    service_response = await service.get_courses()

    return CoursesResponse(
        courses=[
            CourseSchema(
                exchanger=course.exchanger,
                direction=f"{course.from_currency.value}-{course.to_currency.value}",
                value=course.value,
            )
            for course in service_response
        ]
    )
