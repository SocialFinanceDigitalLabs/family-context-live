def find_service_involvement_count(service, person):
    records = service.service_adult_social_care_records.filter(person=person).count()
    records += service.service_school_records.filter(person=person).count()
    records += service.service_housing_records.filter(person=person).count()
    records += service.service_police_records.filter(person=person).count()
    return records
