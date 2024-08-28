SenML YANG Article
====

### If you've kramdown-rfc and need to compile quickly:

```
$ kdrfc draft.md -r -P; evince draft.pdf &;
```

This markdown file should provide:


What is the problem being solved?
-----


SenML is a popular data representation format for simple sensor measurements. SenML format is well described for encoding into JSON, XML and CBOR. However, IoT devices which use YANG data models for data validation and data exchange, don't have any easy way to incorporate and validate their SenML measurements as SenML does not have a YANG model yet.
Additionally, in absence of a YANG model, low powered devices which send measurements in SenML, cannot use CORECONF representation model without resorting to some sort of intermediate data processing. Thus, if SenML has a YANG model, these low powered devices can descibe their data entirely in YANG, which can further be represented in CORECONF for data-compression and fast-traversal.

How SenML was modeled into YANG?
As described in RFC 8428, SenML is used to represent measurements, largely with a key-value combination. Keys are typically SenML labels, and values are actual sensor measurements. Each label has a well-defined data-type for encoding in JSON, in CBOR or in XML [section 12.2 RFC 8428](https://www.rfc-editor.org/rfc/rfc8428#section-12.2).
Hence, to describe a generic SenML model in YANG, it is necessary to represent each of this label as a YANG leaf with the most appropriate YANG type assosciated with the label.

* leaf bn: Base Name which is directly mapped to String
* leaf bt: 
    Base Time which is mapped to closest type available in YANG, 64bits unsigned integer. 
* leaf bu: 
    Base Unit which can be mapped to string type in YANG with special rules where units can be restricted to ones listed in [primary units in RFC 8428](https://www.rfc-editor.org/rfc/rfc8428#section-12.1) or can be extended to support [secondary units described in RFC 8798](https://www.rfc-editor.org/rfc/rfc8798.html#secondary-unit-tbl).

* leaf bv: 
    Base Value which can be mapped to decimal64 type in YANG, with precision of 10 digits. This can be overriden using redefine keyword when this YANG module is imported. 
* leaf bs: 
    Base Sum, live Base Value, can be mapped to decimal64 type and its precision can be overriden later.
* leaf bver: 
    Base Version, which is a positive integer can be modeled as either as a uint8, unit16, unit32 or uint64.

* leaf n:
    Name, modeled as string.

* leaf u:
    Unit, modeled as string.

* leaf v,vs,vb,vd: 
    Value, Value String, Value Boolean and Value Data, modelled as a choice type as exactly one field must appear unless there is a sum field, in which case it is allowed to have no value fields.
* leaf s: 
    Sum, mapped as a decimal64 with 10 digit precision.
* leaf t: 
    Time, mapped as a decimal64 with 10 digit precision. It is optional in SenML to provide time value. However, time leaf is mandatory in YANG if measurement lists are used as it modeled as the key for the measurements. 
* leaf ut:
    Update Time, mapped as a decimal64 with 10 digit precision.
* list e:
    SenML measurement lists, labeled here as "e" is mapped as a list type in YANG with constraint on time as the key.


SenML YANG Model
----
```
module senml {
  yang-version 1.1;
  namespace "urn:ietf:params:xml:ns:yang:senml";

  prefix sen;

  organization
    "LWM2M Working Group";

  typedef UnsignedInteger {
    type union{
      type uint8;
      type uint16;
      type uint32;
      type uint64;
    }
  }

  grouping senml-grouping {
    leaf bn {
      type string;
      mandatory true;
    }

    leaf bt {
      type uint64;
      mandatory true;
    }
    leaf bu {
      type string;
      must "(. = 'm' or . = 'kg' or . = 'g' or . = 's' or . = 'A' or . = 'K' 
      or . = 'cd' or . = 'mol' or . = 'Hz' or . = 'rad' or . = 'sr' or . = 'N' 
      or . = 'Pa' or . = 'J' or . = 'W' or . = 'C' or . = 'V' or . = 'F' or . = 'Ohm' 
      or . = 'S' or . = 'Wb' or . = 'T' or . = 'H' or . = 'Cel' or . = 'lm' or . = 'lx' 
      or . = 'Bq' or . = 'Gy' or . = 'Sv' or . = 'kat' or . = 'm2' or . = 'm3' 
      or . = 'l' or . = 'm/s' or . = 'm/s2' or . = 'm3/s' or . = 'l/s' or . = 'cd/m2' 
      or . = 'W/m2' or . = 'bit' or . = 'bit/s' or . = 'lat' or . = 'lon' or . = 'pH' 
      or . = 'dB' or . = 'dBW' or . = 'Bspl' or . = 'count' or . = '/' or . = '%' 
      or . = '%RH' or . = '%EL' or . = 'EL' or . = '1/s' or . = '1/min' or . = 'beat/min' 
      or . = 'beats' or . = 'S/m' )" {
        description
          "The unit must be from the approved unit list";
        error-message
          "Invalid unit. Unit must be one from SenML Units Registry";
      }
    }

    leaf bv {
      type decimal64{
        fraction-digits "10";
      }
    }

    leaf bs {
      type decimal64{
        fraction-digits "10";
      }
    }

    leaf bver {
      type UnsignedInteger;
      default 10;
    }

    leaf n {
      type string;
    }

    leaf u {
      type string;
      mandatory false;
    }

    choice valueleaf {
      description
        "Exactly one Value field MUST appear unless there is a
         Sum field, in which case it is allowed to have no Value field";
      leaf v {
        type decimal64{
          fraction-digits 10;
        }
      }

      leaf vs {
        type string;
      }

      leaf vb {
        type boolean;
      }

      leaf vd {
        type string;
      }
    }

    leaf s {
      type decimal64{
        fraction-digits "10";
      }
      mandatory false;
    }

    leaf t {
      type decimal64{
        fraction-digits "10";
      }
    }

    leaf ut {
      type decimal64{
        fraction-digits "10";
      }
      mandatory false;
    }
  }

  list e {
    key t;
    uses senml-grouping;
    min-elements 0;
    max-elements unbounded;
  }
}
```


Use case for Senml YANG model
----

An example YANG model is designed for a low cost Long Range (LoRa) device is demonstrated in this section. This model imports two YANG models- [ietf-lora@2016-06-01](https://www.yangcatalog.org/api/services/tree/ietf-lora@2016-06-01.yang) and aforementioned senml.yang

This sensor sends certain parameters critical to its wireless operation such channel-bandwidth, coding rate and spreading factor. Additionally, the sensors wishes to send sensorial data (say temperature readings) in SenML format. Thus the sensor data can be modelled as follows:

```
module lora-sensor-senml {
    yang-version 1.1;
    namespace "urn:ietf:params:xml:ns:yang:lora-sensor";
    prefix "lss";

    import senml {
        prefix lss-senml;
    }

    import ietf-lora {
        prefix lss-ietf-lora;
    }

    container senml-readings {
        uses lss-senml:senml-grouping {
            refine bver {
                default 11;
            }
        }
    }

    augment "/lss:senml-readings" {
        uses lss-ietf-lora:mode;
    }
}
```

The pyang tool can be used to represent the YANG tree:
```
$ pyang -f tree lora-sensor-senml.yang 
module: lora-sensor-senml
  +--rw lora
     +--rw senml-readings* [t]
     |  +--rw bn          string
     |  +--rw bt          uint64
     |  +--rw bu?         string
     |  +--rw bv?         decimal64
     |  +--rw bs?         decimal64
     |  +--rw bver?       UnsignedInteger
     |  +--rw n?          string
     |  +--rw u?          string
     |  +--rw (valueleaf)?
     |  |  +--:(v)
     |  |  |  +--rw v?    decimal64
     |  |  +--:(vs)
     |  |  |  +--rw vs?   string
     |  |  +--:(vb)
     |  |  |  +--rw vb?   boolean
     |  |  +--:(vd)
     |  |     +--rw vd?   string
     |  +--rw s?          decimal64
     |  +--rw t           decimal64
     |  +--rw ut?         decimal64
     +--rw channel-bandwidth?   enumeration
     +--rw coding-rate?         enumeration
     +--rw spreading-factor?    uint8

```

Future, what can be improved in the YANG model

1. Base units can be either enumerated or use identityref types so they can be assigned a SID value.
2. Constraints on having leaves v, vs, vb, vd optional if s is available.
3. Add secondary units described in [RFC 8798](https://www.rfc-editor.org/rfc/rfc8798.html#section-3)in the base units constraints.
-----

