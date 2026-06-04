"""
Replace old image domains in DB with a new domain.

Usage:
    python replace_domain.py <new_domain>

Example:
    python replace_domain.py https://mynewsite.com

Old domains replaced:
    - https://www.linq-staging-site.com/
    - https://harsh7541.pythonanywhere.com/
"""

import os
import sys
import django

def main():
    if len(sys.argv) < 2:
        print("Usage: python replace_domain.py <new_domain>")
        print("Example: python replace_domain.py https://mynewsite.com")
        sys.exit(1)

    new_domain = sys.argv[1].rstrip("/")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
    django.setup()

    from Event.models import (
        eventDetails, eventSpeakers, eventPastAttandees,
        eventSponsors, relatedEvents, eventAgenda,
        eventLeaders, eventSlideShares, pageSeoSettings,
    )
    from Myadmin.models import (
        homePageNavLogoData, homePageVideoSectionInput,
        homePageThirdSection, companiesLogoSection,
        venuePageGallery, generalNewsPoint,
    )

    OLD_DOMAINS = [
        "https://www.linq-staging-site.com",
        "https://harsh7541.pythonanywhere.com",
    ]

    # (ModelClass, field_name)
    MODEL_FIELDS = [
        (eventDetails,              "favicon"),
        (eventSpeakers,             "eventSpeakerHomePageImage"),
        (eventSpeakers,             "eventSpeakerProfilePageImage"),
        (eventSpeakers,             "eventSpeakerFeaturedPageImage"),
        (eventPastAttandees,        "pastAttandeeLogo"),
        (eventSponsors,             "sponsorComapnyLogo"),
        (relatedEvents,             "eventImage"),
        (relatedEvents,             "eventHoverImage"),
        (eventAgenda,               "singleSpeakerAgendaImg"),
        (eventAgenda,               "singleSpeakerCompanyImg"),
        (eventAgenda,               "Speaker1CompanyImg"),
        (eventAgenda,               "Speaker2CompanyImg"),
        (eventLeaders,              "leaderLogo"),
        (eventSlideShares,          "pptImage"),
        (pageSeoSettings,           "pageOgImage"),
        (homePageNavLogoData,       "whiteLogoLink"),
        (homePageNavLogoData,       "blackLogoLink"),
        (homePageVideoSectionInput, "videoLinkmp4"),
        (homePageVideoSectionInput, "videoLinkwebm"),
        (homePageVideoSectionInput, "eventDetailBackImage"),
        (homePageVideoSectionInput, "videoReplaceImage"),
        (homePageVideoSectionInput, "eventStataticsBackImage"),
        (homePageVideoSectionInput, "eventExpertSpeakerBackImage"),
        (homePageThirdSection,      "thirdSectionBackgroundImage"),
        (companiesLogoSection,      "logoLink"),
        (venuePageGallery,          "gallerySectionOneBigImage"),
        (venuePageGallery,          "gallerySectionOneSmallImage"),
        (venuePageGallery,          "gallerySectionTwoBigImage"),
        (venuePageGallery,          "gallerySectionTwoSmallImage"),
        (venuePageGallery,          "gallerySectionThreeBigImage"),
        (venuePageGallery,          "gallerySectionThreeSmallImage"),
        (generalNewsPoint,          "newsImage"),
    ]

    total_updated = 0

    for model_cls, field_name in MODEL_FIELDS:
        model_name = model_cls.__name__
        field_filter = {f"{field_name}__isnull": False}
        records = model_cls.objects.filter(**field_filter).exclude(
            **{field_name: ""}
        )

        updated_count = 0
        for record in records:
            value = getattr(record, field_name)
            if not value or not isinstance(value, str):
                continue

            new_value = value
            for old_domain in OLD_DOMAINS:
                if old_domain in new_value:
                    new_value = new_value.replace(old_domain, new_domain)

            if new_value != value:
                setattr(record, field_name, new_value)
                record.save(update_fields=[field_name])
                updated_count += 1

        if updated_count:
            print(f"  [{model_name}.{field_name}] updated {updated_count} record(s)")
        total_updated += updated_count

    print(f"\nDone. Total records updated: {total_updated}")


if __name__ == "__main__":
    main()
