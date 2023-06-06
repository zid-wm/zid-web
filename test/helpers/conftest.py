VATSIM_STATUS = {
    'data': {
        'v3': [
            'https://data.vatsim.net/v3/vatsim-data.json'
        ],
        'servers': [
            'https://data.vatsim.net/v3/vatsim-servers.json'
        ]
    },
    'user': [
        'https://stats.vatsim.net/search_id.php'
    ],
    'metar': [
        'http://metar.vatsim.net/metar.php'
    ]
}

VATSIM_DATA = {
    "general": {
        "version": 3,
        "reload": 1,
        "update": "20230511015914",
        "update_timestamp": "2023-05-11T01:59:14.0215902Z",
        "connected_clients": 631,
        "unique_users": 581
    },
    "pilots": [
        {
            "cid": 1021284,
            "name": "Guilherme Trancoso SBJR",
            "callsign": "KAL42",
            "server": "USA-EAST2",
            "pilot_rating": 1,
            "military_rating": 0,
            "latitude": 37.57105,
            "longitude": 138.01183,
            "altitude": 28226,
            "groundspeed": 426,
            "transponder": "7440",
            "heading": 249,
            "qnh_i_hg": 30.14,
            "qnh_mb": 1021,
            "flight_plan": {
                "flight_rules": "I",
                "aircraft": "B77W/H-VGDW/C",
                "aircraft_faa": "H/B77W/L",
                "aircraft_short": "B77W",
                "departure": "KSEA",
                "arrival": "RKSI",
                "alternate": "RKPK",
                "cruise_tas": "494",
                "altitude": "26000",
                "deptime": "1500",
                "enroute_time": "1120",
                "fuel_time": "1256",
                "remarks":
                    "PBN/A1B1C1D1L1O1S1 NAV/RNVD1E2A1 DOF/230510 REG/HL7783EET/CZVR0018 "
                    "PAZA0121 RJJJ0619 RKRR1010 SEL/EPGH RVR/75 OPR/KOREAN AIR PER/D /V/",
                "route":
                    "+BANGR9 ARRIE J523 TOU J501 YAZ Q801 FINGS KATCH 55N140W 60N160W NEONN "
                    "G349 MARCC R338 NATES R220 NRKEY/N0495F280 R220 NODAN/N0489F300 R217 "
                    "GTC Y142 SAMON SAPRA Y685 CUN CUN2M",
                "revision_id": 2,
                "assigned_transponder": "7440"
            },
            "logon_time": "2023-05-10T15:22:08Z",
            "last_updated": "2023-05-11T01:59:10.5482293Z"
        },
        {
            "cid": 1339761,
            "name": "Gabriel Simões SBPL",
            "callsign": "AZU8700",
            "server": "USA-EAST",
            "pilot_rating": 0,
            "military_rating": 0,
            "latitude": 36.45356,
            "longitude": -14.32042,
            "altitude": 36219,
            "groundspeed": 485,
            "transponder": "2000",
            "heading": 17,
            "qnh_i_hg": 30.18,
            "qnh_mb": 1022,
            "flight_plan": {
                "flight_rules": "I",
                "aircraft": "A359/H-SDE1FGHIJ1RWXYZ/LB1",
                "aircraft_faa": "H/A359/L",
                "aircraft_short": "A359",
                "departure": "SBKP",
                "arrival": "LFPO",
                "alternate": "EGLL",
                "cruise_tas": "481",
                "altitude": "31000",
                "deptime": "1720",
                "enroute_time": "1213",
                "fuel_time": "1421",
                "remarks":
                    "PBN/A1B1C1D1L1O1S1 NAV/RNVD1E2A1 DOF/230510 REG/PRAOY EET/SBBS0017 "
                    "SBRE0109 SBAO0312 GOOO0412 GVSC0531 GCCC0636 LPPC0803 LECM0932 EGGX0951 "
                    "EISN1041 EGTT1103 LFFF1143 SEL/ABCD OPR/AZUL PER/D RMK/FLYAZULV AZU4743 /V/",
                "route":
                    "KONVI UZ23 BHZ UZ61 QUARU/N0477F330 UN866 OBKUT/N0473F350 UN866 "
                    "TENPA/N0472F360 UN866 GOMER UN981 BIMBO DCT OBESA DCT PETEK/N0470F380 "
                    "DCT BERUX/M082F370 T213 TAMEL DCT EVBAK DCT LIFFY/N0470F370 UL975 MALUD "
                    "L15 KEPAD L151 KIDLI UN859 LGL A34 BOBSA",
                "revision_id": 1,
                "assigned_transponder": "0000"
            },
            "logon_time": "2023-05-10T17:13:15Z",
            "last_updated": "2023-05-11T01:59:09.9586589Z"
        }
    ],
    "controllers": [
        {
            "cid": 123456,
            "name": "FirstName LastName",
            "callsign": "SDF_TWR",
            "frequency": "124.200",
            "facility": 4,
            "rating": 4,
            "server": "CANADA",
            "visual_range": 50,
            "text_atis": None,
            "last_updated": "2023-05-11T01:59:03.4676778Z",
            "logon_time": "2023-05-10T19:03:47Z"
        },
        {
            "cid": 111111,
            "name": "First Last",
            "callsign": "IND_CTR",
            "frequency": "119.550",
            "facility": 6,
            "rating": 5,
            "server": "GERMANY",
            "visual_range": 300,
            "text_atis": [
                "Line1",
                "Line2",
                "Line3"
            ],
            "last_updated": "2023-05-11T01:59:02.6850431Z",
            "logon_time": "2023-05-10T19:16:16Z"
        },
        {
            "cid": 987654,
            "name": "Fname Lname",
            "callsign": "CLE_CTR",
            "frequency": "133.650",
            "facility": 6,
            "rating": 5,
            "server": "CANADA",
            "visual_range": 300,
            "text_atis": [
                "Line1",
                "Line2",
                "Line3"
            ],
            "last_updated": "2023-05-11T01:59:09.456467Z",
            "logon_time": "2023-05-10T19:36:03.4858694Z"
        }
    ],
    "atis": [
        {
            "cid": 111111,
            "name": "First Last",
            "callsign": "KCVG_ATIS",
            "frequency": "123.450",
            "facility": 4,
            "rating": 5,
            "server": "GERMANY",
            "visual_range": 50,
            "atis_code": "N",
            "text_atis": [
                "LINE1",
                "LINE2",
                "LINE3",
                "LINE4",
                "LINE5"
            ],
            "last_updated": "2023-05-11T01:58:59.3091237Z",
            "logon_time": "2023-05-10T22:30:59.3946021Z"
        },
    ],
    "servers": [
        {
            "ident": "CANADA",
            "hostname_or_ip": "159.203.44.51",
            "location": "Toronto, Canada",
            "name": "CANADA",
            "clients_connection_allowed": 1,
            "client_connections_allowed": True,
            "is_sweatbox": False
        },
        {
            "ident": "GERMANY",
            "hostname_or_ip": "178.128.193.227",
            "location": "Frankfurt, Germany",
            "name": "GERMANY",
            "clients_connection_allowed": 1,
            "client_connections_allowed": True,
            "is_sweatbox": False
        }
    ],
    "prefiles": [], # Might need to be mocked for IDS testing in the future
    "facilities": [
        {
            "id": 0,
            "short": "OBS",
            "long": "Observer"
        },
        {
            "id": 1,
            "short": "FSS",
            "long": "Flight Service Station"
        },
        {
            "id": 2,
            "short": "DEL",
            "long": "Clearance Delivery"
        },
        {
            "id": 3,
            "short": "GND",
            "long": "Ground"
        },
        {
            "id": 4,
            "short": "TWR",
            "long": "Tower"
        },
        {
            "id": 5,
            "short": "APP",
            "long": "Approach/Departure"
        },
        {
            "id": 6,
            "short": "CTR",
            "long": "Enroute"
        }
    ],
    "ratings": [
        {
            "id": -1,
            "short": "INAC",
            "long": "Inactive"
        },
        {
            "id": 0,
            "short": "SUS",
            "long": "Suspended"
        },
        {
            "id": 1,
            "short": "OBS",
            "long": "Observer"
        },
        {
            "id": 2,
            "short": "S1",
            "long": "Tower Trainee"
        },
        {
            "id": 3,
            "short": "S2",
            "long": "Tower Controller"
        },
        {
            "id": 4,
            "short": "S3",
            "long": "Senior Student"
        },
        {
            "id": 5,
            "short": "C1",
            "long": "Enroute Controller"
        },
        {
            "id": 6,
            "short": "C2",
            "long": "Controller 2 (not in use)"
        },
        {
            "id": 7,
            "short": "C3",
            "long": "Senior Controller"
        },
        {
            "id": 8,
            "short": "I1",
            "long": "Instructor"
        },
        {
            "id": 9,
            "short": "I2",
            "long": "Instructor 2 (not in use)"
        },
        {
            "id": 10,
            "short": "I3",
            "long": "Senior Instructor"
        },
        {
            "id": 11,
            "short": "SUP",
            "long": "Supervisor"
        },
        {
            "id": 12,
            "short": "ADM",
            "long": "Administrator"
        }
    ],
    "pilot_ratings": [
        {
            "id": 0,
            "short_name": "NEW",
            "long_name": "Basic Member"
        },
        {
            "id": 1,
            "short_name": "PPL",
            "long_name": "Private Pilot License"
        },
        {
            "id": 3,
            "short_name": "IR",
            "long_name": "Instrument Rating"
        },
        {
            "id": 7,
            "short_name": "CMEL",
            "long_name": "Commercial Multi-Engine License"
        },
        {
            "id": 15,
            "short_name": "ATPL",
            "long_name": "Airline Transport Pilot License"
        },
        {
            "id": 31,
            "short_name": "FI",
            "long_name": "Flight Instructor"
        },
        {
            "id": 63,
            "short_name": "FE",
            "long_name": "Flight Examiner"
        }
    ],
    "military_ratings": [
        {
            "id": 0,
            "short_name": "M0",
            "long_name": "No Military Rating"
        },
        {
            "id": 1,
            "short_name": "M1",
            "long_name": "Military Pilot License"
        },
        {
            "id": 3,
            "short_name": "M2",
            "long_name": "Military Instrument Rating"
        },
        {
            "id": 7,
            "short_name": "M3",
            "long_name": "Military Multi-Engine Rating"
        },
        {
            "id": 15,
            "short_name": "M4",
            "long_name": "Military Mission Ready Pilot"
        }
    ]
}
