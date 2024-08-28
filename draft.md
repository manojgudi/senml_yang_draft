---
stand_alone: true
ipr: trust200902
docname: draft-t2t-senml-as-coreconf
cat: std
pi:
  symrefs: 'yes'
  sortrefs: 'yes'
  strict: 'yes'
  compact: 'yes'
  toc: 'yes'

title: Representing SenML in CORECONF Format
abbrev: SenML CORECONF
wg: t2t Research Group
author:

- ins: M. Gudi
  name: Manoj Gudi
  org: Institut MINES TELECOM; IMT Atlantique
  street:
  - 2 rue de la Chataigneraie
  - CS 17607
  city: 35576 Cesson-Sevigne Cedex
  country: France
  email: manoj.gudi@imt-atlantique.net

- ins: L. Toutain
  name: Laurent Toutain
  org: Institut MINES TELECOM; IMT Atlantique
  street:
  - 2 rue de la Chataigneraie
  - CS 17607
  city: 35576 Cesson-Sevigne Cedex
  country: France
  email: Laurent.Toutain@imt-atlantique.fr

normative:
  RFC8428:
  RFC8798:
  RFC8949:
  RFC8428:
  RFC7950:
  RFC9254:
  RFC8259:
  RFC6095:
  I-D.ietf-core-sid:
  I-D.ietf-core-comi:
  I-D.toutain-t2t-sid-extension:

--- abstract

SenML is one of the most popular data formats used by the Internet-of-Things (IoT) devices to send simple sensor readings and device parameters over the network. However, a lack of a YANG model for SenML means it cannot be used with applications which already conform to YANG models. Furthermore, some of the encoding-formats and tools available for YANG models, cannot be extended to devices sending data in SenML format. This document outlines a possible YANG model for SenML format, and illustrates an example of a sensor device which leverages this model to concisely represent its SenML data in CORECONF format.
--- middle

# Introduction

In its simplest form, an IoT device typically consists of at least one sensor, and ability to send this sensor measurements over the network. Occassionally, the device parameters can also be sent over the network to monitor and manipulate this its behavior. Such devices are also constrained on energy, network (in its availability as well as bandwidth), and data processing capabilities as they employ primitive processors. Consequently, SenML is an apt choice for representing this nature of data from these devices.

However, as much as SenML is useful in building simple IoT applications, a well-defined data model for the same would allow developers and engineers alike to build more complex data systems if SenML can be represented as a YANG model. Subsequently, the YANG model of SenML can leverage SID based CORECONF representation of its data to further reduce network footprint and improve its inter-operability with other network devices.

# SenML Format

SenML or Sensor Measurement Lists is an application layer formatting used typically by the constrained devices to send sensorial information over the networks {{RFC8428}}. This format is aimed at reducing redundancies in the information sent over the network by introducing concepts such as base-name, base-unit, base-version, base-time and base-value. Moreover, the format specifies how the application payload can be serialized in three popular formats before sending it over the network- JSON (JavaScript Object Notation) {{RFC8259}}, CBOR (Concise Binary Object Representation){{RFC8949}} and XML (Extensible Markup Language).

Although SenML record has a well-defined Concise Data Definition Language (CDDL) for JSON and CBOR representations in section 11 of {RFC8428}}, the lack of an accompanying data model means it is harder to use SenML for applications with strict requirement for data organization and data validation. Additionally, SenML format needs more work to integrate with messages which have well defined data models. Finally, SenML CDDL cannot be used directly to extend to other  data formats such as CoAP Management Interface (CORECONF){{I-D.ietf-core-comi}}.

# YANG Model Language

YANG or Yet Another Next Generation is data modelling language used to describe the organization and constraints of configuration and state data of the network elements. This data is typically exchanged using NETCONF or RESTCONF protocols {{RFC7950}}. YANG boasts of rich data types and language features to represent constraints on data as rules useful for data-validation. These models often are considered de-facto interchange formats for a particular protocol (or application) which allows network device manufaturers to build interoperable devices. Additionally, YANG supports several language extensions for constructing user-defined data types, recursive data models and allowing inheritance to reuse existing data models {{RFC6095}}.


YANG entails organizing application data in hierarchical tree like format. The fundamental element of a YANG module which contains data is called a leaf, and each leaf is associated with a well-defined data type. The relationship between these leaves are modelled using elements such as containers, lists, grouping, choice etc. The entire YANG model can be visualized as a tree using helpful tools such as pyang. YANG models also outline a way to encode into popular serialization formats such as JSON, CBOR and XML in {{RFC9254}}.

To enable accurate, fast and efficient transmission of data conformant to YANG models, Schema Identifiers (known as SIDs) can be generated and assigned for each YANG element {{I-D.ietf-core-sid}} . These SIDs can be used to transform data in CORECONF format as demonstrated in {{I-D.toutain-t2t-sid-extension}}. An example of this is also described in section 6 below.

As aforementioned, SenML format is well described for encoding into JSON, XML and CBOR. However, IoT devices which use YANG data models for data validation and data exchange, don't have any easy way to incorporate and validate their SenML measurements as SenML does not have a YANG model yet. Additionally, in absence of a YANG model, low powered devices which send measurements in SenML, cannot use CORECONF representation model without resorting to some sort of intermediate data processing. Thus, if SenML has a YANG model, these low powered devices can descibe their data entirely in YANG, which can further be represented in CORECONF for data-compression and fast-traversal.

# YANG Model for SenML: Considerations

As described in RFC 8428, SenML is used to represent measurements, largely with a key-value combination. Keys are typically SenML labels, and values are actual sensor measurements. Each label has a well-defined data-type for encoding in JSON, in CBOR or in XML [section 12.2 RFC 8428](https://www.rfc-editor.org/rfc/rfc8428#section-12.2).
Hence, to describe a generic SenML model in YANG, it is necessary to represent each of this label as a YANG leaf with the most appropriate YANG type assosciated with the label.

* bn:<br />
    Base Name which is directly mapped to String
* bt:<br />
    Base Time which is mapped to closest type available in YANG, 64bits unsigned integer. 
* bu:<br />
    Base Unit which can be mapped to string type in YANG with special rules where units can be restricted to ones listed in Section 12.1 (primary units) of {{RFC8428}} or can be extended to support secondary units described Section 3 in {{RFC8798}}.

* bv:<br />
    Base Value which can be mapped to decimal64 type in YANG, with precision of 10 digits. This can be overriden using redefine keyword when this YANG module is imported. 
* bs:<br />
    Base Sum, live Base Value, can be mapped to decimal64 type and its precision can be overriden later.
* bver:<br />
    Base Version, which is a positive integer can be modeled as either as a uint8, unit16, unit32 or uint64.

* n:<br />
    Name, modeled as string.

* u:<br />
    Unit, modeled as string.

* leaves v,vs,vb,vd:<br />
    Value, Value String, Value Boolean and Value Data, modelled as a choice type as exactly one field must appear unless there is a sum field, in which case it is allowed to have no value fields.
* s:<br />
    Sum, mapped as a decimal64 with 10 digit precision.
* t:<br />
    Time, mapped as a decimal64 with 10 digit precision. It is optional in SenML to provide time value. However, time leaf is mandatory in YANG if measurement lists are used as it modeled as the key for the measurements. 
* ut:<br />
    Update Time, mapped as a decimal64 with 10 digit precision.
* list e:<br />
    SenML measurement lists, labeled here as "e" is mapped as a list type in YANG with constraint on time as the key.


# YANG Model for SenML: Implementation

~~~~
<CODE BEGINS> file "senml.yang"
{::include senml.yang}
<CODE ENDS>
~~~~

# Transforming SenML to CORECONF


An example YANG model is designed for a low cost Long Range (LoRa) device is demonstrated in this section. This model imports two YANG models- [ietf-lora@2016-06-01](https://www.yangcatalog.org/api/services/tree/ietf-lora@2016-06-01.yang) and aforementioned senml.yang

This sensor sends certain parameters critical to its wireless operation such channel-bandwidth, coding rate and spreading factor. Additionally, the sensors wishes to send sensorial data (say temperature readings) in SenML format. Thus the sensor data can be modelled as follows:

~~~~
<CODE BEGINS> file "lora-sensor-senml.yang"
{::include lora-sensor-senml.yang}
<CODE ENDS>
~~~~


The pyang tool can be used to visualize the YANG tree:

~~~~
$ pyang -f tree lora-sensor-senml.yang
module: lora-sensor-senml
  +--rw e* [t]
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
  +--rw lora
     +--rw channel-bandwidth?   enumeration
     +--rw coding-rate?         enumeration
     +--rw spreading-factor?    uint8
~~~~

An example instance of JSON data instance for the above YANG model is presented below:

~~~~
<CODE BEGINS> file "senml_example_lora.json"
{::include senml_example_lora.json}
<CODE ENDS>
~~~~

Next, for the above YANG model, we can generate the SIDs using pyang tool starting from integer 60000, as follows:

~~~~
$ pyang --sid-extension --sid-generate-file=60000:100 --sid-list lora-sensor-senml.yang

SID        Assigned to
---------  --------------------------------------------------
60000      module lora-sensor-senml
60001      data /lora-sensor-senml:e
60002      data /lora-sensor-senml:e/bn
60003      data /lora-sensor-senml:e/bs
60004      data /lora-sensor-senml:e/bt
60005      data /lora-sensor-senml:e/bu
60006      data /lora-sensor-senml:e/bv
60007      data /lora-sensor-senml:e/bver
60008      data /lora-sensor-senml:e/n
60009      data /lora-sensor-senml:e/s
60010      data /lora-sensor-senml:e/t
60011      data /lora-sensor-senml:e/u
60012      data /lora-sensor-senml:e/ut
60013      data /lora-sensor-senml:e/v
60014      data /lora-sensor-senml:e/vb
60015      data /lora-sensor-senml:e/vd
60016      data /lora-sensor-senml:e/vs
60017      data /lora-sensor-senml:lora
60018      data /lora-sensor-senml:lora/channel-bandwidth
60019      data /lora-sensor-senml:lora/coding-rate
60020      data /lora-sensor-senml:lora/spreading-factor

File lora-sensor-senml@unknown.sid created
Number of SIDs available : 100
Number of SIDs used : 21
~~~~

The COORECONF diagnostic format of the JSON data instance is shown below:

~~~~
{60001: [{1: 'urn:dev:ow:10e2073a0108006:',
          3: 1320078429,
          7: 'temperature',
          10: 'Cel',
          12: 23.1},
         {7: 'humidity',
          10: '%RH',
          12: 67.3}],
 60017: {1: 0, 2: 1, 3: 7}}
~~~~

Finally, comparing the JSON with the corresponding CORECONF-CBOR encoded form, is shown below:

~~~~
CBOR Hex:

a219ea6182a501781b75726e3a6465763a6f773a3130653230373361303130383030363a031a4eaecc5d076b74656d70657261747572650a6343656c0cfb403719999999999aa3076868756d69646974790a632552480cfb4050d3333333333319ea71a3010003070201


JSON size: 207 Bytes | CORECONF size: 106 Bytes | Compressed: ≈ 48.79%
~~~~


# Further work

Three primary areas of future work have been identified to improve SenML YANG modelling- 

1. Base units can be either modelled as enumerated type or identityref type, so they can be assigned a SID value. This should ideally further reduce the CORECONF-CBOR encoded message.
2. Constraints on having leaves v, vs, vb, vd optional if s is available as described in Section 4.2 of {{RFC8428}}
3. Add secondary units described in {{RFC8798}} in the base units constraints.



