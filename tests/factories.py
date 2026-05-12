import factory
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from django.utils import timezone
from users.models import *
from core.models import *
from services.constants import *

class BaseFactory(DjangoModelFactory):

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = super()._create(model_class, *args, **kwargs)

        print(
            f"\n[FACTORY CREATED] "
            f"{model_class.__name__} "
            f"(id={getattr(obj, 'id', None)}) -> {obj}"
        )

        return obj


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    role = Role.PATIENT

    gender = Faker(
        "random_element",
        elements=[
            Gender.MALE,
            Gender.FEMALE,
        ],
    )

    date_of_birth = Faker("date_of_birth")
    phone = Faker(
        "numerify",
        text="##########"
    )

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "TestPassword123"
        self.set_password(password)

        if create:
            self.save()


class PatientFactory(BaseFactory):
    class Meta:
        model = Patient
        django_get_or_create = ("user",)

    user = SubFactory(
        UserFactory,
        role=Role.PATIENT,
    )

class DoctorFactory(BaseFactory):
    class Meta:
        model = Doctor
        django_get_or_create = ("user",)

    user = SubFactory(
        UserFactory,
        role=Role.DOCTOR,
    )

    specialization = Faker("job")



class NurseFactory(BaseFactory):
    class Meta:
        model = Nurse
        django_get_or_create = ("user",)

    user = SubFactory(
        UserFactory,
        role=Role.NURSE,
    )



class StaffFactory(BaseFactory):
    class Meta:
        model = Staff
        django_get_or_create = ("user",)

    user = SubFactory(
        UserFactory,
        role=Role.STAFF,
    )


class AppointmentFactory(BaseFactory):
    class Meta:
        model = Appointment

    doctor = SubFactory(DoctorFactory)
    patient = SubFactory(PatientFactory)

    scheduled_at = Faker(
        "date_time_between",
        start_date="now",
        end_date="+30d",
        tzinfo=timezone.get_current_timezone(),
    )

    reason = Faker("sentence")

    status = Faker(
        "random_element",
        elements=[
            AppointmentChoices.SCHEDULED,
            AppointmentChoices.COMPLETED,
            AppointmentChoices.CANCELLED,
        ],
    )


class PrescriptionFactory(BaseFactory):
    class Meta:
        model = Prescription

    patient = SubFactory(PatientFactory)

    doctor = SubFactory(DoctorFactory)

    appointment = SubFactory(AppointmentFactory)

    medicines = Faker(
        "sentence",
        nb_words=3,
    )

    notes = Faker("sentence")


class LabReportFactory(BaseFactory):
    class Meta:
        model = LabReport

    patient = SubFactory(PatientFactory)

    ordered_by = SubFactory(DoctorFactory)

    test_name = Faker(
        "random_element",
        elements=[
            "Blood Test",
            "X-Ray",
            "MRI",
            "CT Scan",
        ],
    )

    result = Faker("sentence")

    status = Faker(
        "random_element",
        elements=[
            LabReportChoices.PENDING,
            LabReportChoices.READY,
        ],
    )


class VitalsFactory(BaseFactory):
    class Meta:
        model = Vitals

    patient = SubFactory(PatientFactory)

    recorded_by = SubFactory(NurseFactory)


    pulse = Faker(
        "random_int",
        min=60,
        max=120,
    )

    temperature = Faker(
        "pyfloat",
        left_digits=2,
        right_digits=1,
        positive=True,
        min_value=36,
        max_value=40,
    )

    weight = Faker(
        "pyfloat",
        left_digits=3,
        right_digits=1,
        positive=True,
        min_value=40,
        max_value=120,
    )

    blood_pressure = Faker(
        "random_element",
        elements=[
            "120/80",
            "110/70",
            "130/85",
        ],
    )

