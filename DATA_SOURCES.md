# Facility directory data

## Current map state

The dashboard contains 15 curated European **metro-level reference locations**. They are suitable for demonstrating map interaction only. They are not a facility directory and must not be represented as live operations, capacity, carbon intensity, PUE, renewable mix, or availability.

## Proposed production source: PeeringDB

GeoDataViewer's data-centers map identifies PeeringDB as its source. Flaer must use the PeeringDB API directly rather than scrape GeoDataViewer.

Before importing or publishing a bulk facility directory, obtain written approval from PeeringDB. Their acceptable-use policy restricts bulk redistribution and commercial mapping.

When approval is received, the importer must store these fields with every record:

- `source`: `PeeringDB`
- `source_record_id`
- `source_url`
- `retrieved_at`
- `licence_or_permission_reference`
- `country`, `city`, `latitude`, `longitude`, `facility_name`, `operator`
- `verification_status`: `directory-listed` (not `operationally-verified`)

## Approval request email

Send this to `support@peeringdb.com`:

> Subject: Request to use PeeringDB facility directory data in Flaer
>
> Hello PeeringDB team,\n\nFlaer is a Europe-focused sustainability workspace for data-centre operators. We would like permission to periodically retrieve and display selected European facility directory fields from the PeeringDB API: facility name, organisation/operator, city, country, coordinates, PeeringDB ID, and source attribution.\n\nWe would not use the data for advertising, sell or redistribute a bulk download, or claim that facility directory entries are real-time operational telemetry. We would display clear PeeringDB attribution and retain source IDs and refresh timestamps.\n\nCould you confirm whether this use is permitted and any required attribution, refresh, caching, or access conditions?\n\nThank you.

## Do not import

- Data copied from visual maps without an API/export licence.
- Carbon, capacity, PUE, renewable, risk, uptime, or availability values unless supplied by a verified owner, operator, or authorised telemetry provider.
- Exact building coordinates where the source or facility operator has not authorised publication.
