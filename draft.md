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

title: SenML is CORECONF!
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

- ins: Alejandro Fernadez
  name: Alejandro Fernadez
  org: Institut MINES TELECOM; IMT Atlantique
  street:
  - 2 rue de la Chataigneraie
  - CS 17607
  city: 35576 Cesson-Sevigne Cedex
  country: France
  email: javier-alejandro.fernandez-cordova@imt-atlantique.net 

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

SenML is one of the data formats used by the Internet-of-Things (IoT) devices to send simple sensor readings and device parameters over the network. However, a lack of a YANG model for SenML means it cannot be used by the applications which already use YANG for data modeling and validation. Furthermore, some of the encoding formats and tools available for YANG models, cannot be used by the devices sending data in SenML format. This document provides one of the ways to model SenML data in YANG. Additionally, SenML data is encoded into CORECONF format using this YANG model to concisely represent the data.

--- middle

# Introduction

In its simplest form, an IoT device consists of at least one sensor, and ability to send measurements of this sensor over the network. Occasionally, the device parameters can also be sent over the network to monitor and manipulate its behavior. Such devices are constrained on energy, network (in its availability as well as bandwidth), and data processing capabilities as they embed primitive processors. Consequently, SenML is an appropriate choice for representing this nature of data from these devices.

As much as SenML is useful in building simple IoT applications, a well-defined data model for the same would allow developers and engineers alike to build more complex data systems if the data can be modeled in YANG. Subsequently, the YANG model of SenML can leverage SID based CORECONF representation of its data to further reduce network footprint and improve its interoperability with other network devices.

# SenML Format

SenML or Sensor Measurement Lists is an data format used by the constrained devices to send sensor information over the networks {{RFC8428}}. These measurements are often structured as key-value pairs where the keys (also known as fields) describe the associated sensor data. Each field has a well defined label, whether it is mandatory to be included and the permitted values it can carry. SenML also reduces sending redundant information over the network by introducing concepts such as base-name, base-unit, base-version, base-time and base-value.

The format specifies how the application payload can be serialized in three popular formats before sending it over the network- JSON (JavaScript Object Notation) {{RFC8259}}, CBOR (Concise Binary Object Representation){{RFC8949}} and XML (Extensible Markup Language).

Although a SenML record has a well-defined Concise Data Definition Language (CDDL) for JSON and CBOR representations in section 11 of {RFC8428}}, the lack of an accompanying data model means it is harder to use it for applications with strict requirement for data organization and validation. Additionally, SenML CDDL cannot be used directly to extend to other  data formats such as CoAP Management Interface (CORECONF){{I-D.ietf-core-comi}}.

# YANG Model Language

YANG or Yet Another Next Generation is data modeling language used to describe the organization and constraints on the configuration and state data of the network devices. This data is typically exchanged using NETCONF or RESTCONF protocols {{RFC7950}}. As YANG models are considered de-facto interchange formats for a particular protocol (or application) which allows network device manufacturers to build inter-operable devices. YANG has rich data types, language features, and supports several extensions for constructing user-defined data types, recursive data models and allowing inheritance to reuse existing data models {{RFC6095}} among others.

<!--
YANG organizes the data hierarchically in a tree format. The fundamental element of a YANG module which contains data is called a leaf, and each leaf is associated with a well-defined data type. The relationship between these leaves are modeled using elements such as containers, lists, grouping, choice etc. The entire YANG model can be visualized as a tree using helpful tools such as pyang. YANG models also outline a way to encode into popular serialization formats such as JSON, CBOR and XML in {{RFC9254}}. 
-->

Logically, to model SenML format into a YANG model, the measurements can be designed as YANG lists and each SenML record is a grouping containing leaves of SenML fields and values {{RFC9254}}. Additional constraints and rules can be added to the model ensure conformance with SenML specification. Visually it can be represented as follows:


|---
| SenML Element | YANG Equivalent
|-|-
| Measurement   | List               
| Field         | Leaf               
| Label         | Leaf Name          
| Value Type    | Leaf Type          
| Record        | Grouping/Container 
|===


Section 11 of {{RFC8428}} specifies how SenML format is described for encoding into JSON, XML and CBOR. However, IoT devices which use YANG data models don't have any easy way to incorporate and validate their SenML measurements. Additionally, in absence of a YANG model, low powered devices which send measurements in SenML, cannot use CORECONF representation model without resorting to some sort of intermediate data processing. Hence, if SenML has a YANG model, these low powered devices can describe their data entirely in it. Their data can further be transformed in CORECONF, which complies with SenML-CBOR encoding rules before transmitting it over the network.

To enable accurate, fast and efficient transmission of data conforming to YANG models, Schema Identifiers (known as SIDs) can be generated and assigned for each YANG element {{I-D.ietf-core-sid}} . These SIDs can be used to transform data in CORECONF format as demonstrated in {{I-D.toutain-t2t-sid-extension}}. An example of this is also described in [Transforming SenML to CORECONF](#transforming-senml-to-coreconf) below.


# YANG Model for SenML: Considerations

As described in {{RFC8428}}, SenML measurements consists of field and a value, and each field is identified by its label (which are different for JSON and CBOR). Each value has a well-defined data-type for encoding in JSON, in CBOR or in XML as outlined in [section 12.2 RFC 8428](https://www.rfc-editor.org/rfc/rfc8428#section-12.2).
Hence, to describe a generic SenML model in YANG, it is necessary to represent each field as a YANG leaf with the most appropriate YANG type associated with the type from the "XML Type" Column.

An user data type is created in the YANG model to make XML Integer like type-definition. XML [Double type](https://www.w3.org/TR/xmlschema11-2/#double) follows [IEEE 754-2008 definition](https://ieeexplore.ieee.org/document/4610935), which results in approximately 15 significant digits. However for the YANG model, XML Double is replaced by a Number type, which is a decimal64 type with 5 precision digits and has a range of \[-92233720368547.75808, 92233720368547.75807\]. This is chosen arbitrarily to balance precision and range in YANG but can be changed by the user later.

* bn:  
    Base Name, which is directly mapped to String
* bt:  
    Base Time, which is mapped to closest type available in YANG, decimal64. 
* bu:  
    Base Unit, which can be mapped to string type in YANG with special rules where units can be restricted to ones listed in Section 12.1 (primary units) of {{RFC8428}} or can be extended to support secondary units described Section 3 in {{RFC8798}}.
* bv:  
    Base Value, which can be mapped to decimal64 type in YANG, with precision of 5 digits. This can be overridden using redefine keyword when this YANG module is imported. 
* bs:  
    Base Sum, live Base Value, can be mapped to decimal64 type and its precision can be overridden later.
* bver:  
    Base Version, which is an integer can be modeled union type to assume either as a int8, int16, int32 or int64 types.

* n:  
    Name, modeled as string.
* u:  
    Unit, modeled as string.

* leaves v,vs,vb,vd:  
    Value, Value String, Value Boolean and Value Data, modeled as a choice type as exactly one field must appear unless there is a sum field, in which case it is allowed to have no value fields.
* s:  
    Sum, mapped as a decimal64 with 5 digit precision.
* t:  
    Time, mapped as a decimal64 with 5 digit precision. Although it is optional in SenML to provide time but for this YANG model, it is mandatory-leaf if measurement lists are used as time is the key for the measurements list (e).
* ut:  
    Update Time, mapped as a decimal64 with 5 digit precision.
* list e:  
    SenML measurement lists, labeled here as "e" (events) is mapped as a list type in YANG with constraint on time (t) as the key. Thus, t has to be present and unique in the measurement lists.


# YANG Model for SenML: Implementation

~~~~
<CODE BEGINS> file "senml.yang"
{::include senml.yang}
<CODE ENDS>
~~~~

The pyang tool can be used to visualize the YANG tree:

~~~~
$ pyang -f tree senml.yang
module: senml
  +--rw e* [t]
     +--rw bn?         string
     +--rw bt?         decimal64
     +--rw bu?         string
     +--rw bv?         decimal64
     +--rw bs?         decimal64
     +--rw bver?       Integer
     +--rw n?          string
     +--rw u?          string
     +--rw (valueleaf)?
     |  +--:(v)
     |  |  +--rw v?    decimal64
     |  +--:(vs)
     |  |  +--rw vs?   string
     |  +--:(vb)
     |  |  +--rw vb?   boolean
     |  +--:(vd)
     |     +--rw vd?   string
     +--rw s?          decimal64
     +--rw t           decimal64
     +--rw ut?         decimal64
~~~~

An example instance of JSON data instance for the above YANG model is presented below:

~~~~
file "senml_example.json"
{::include senml_example.json}
~~~~

It is possible to validate this YANG model against a SenML data in json encoding as shown below using yangson library:

~~~~
<CODE BEGINS> file "validate_senml_yang.py"
{::include validate_senml_yang.py}
<CODE ENDS>
~~~~
{: .language-python}

# Transforming SenML to CORECONF

Next, for the above YANG model, we can generate the SIDs using pyang tool starting from integer 60000, as follows:

~~~~
$ pyang --sid-extension --sid-generate-file=60000:100 --sid-list senml.yang 

SID        Assigned to
---------  --------------------------------------------------
60000      module senml
60001      data /senml:e
60002      data /senml:e/bn
60003      data /senml:e/bs
60004      data /senml:e/bt
60005      data /senml:e/bu
60006      data /senml:e/bv
60007      data /senml:e/bver
60008      data /senml:e/n
60009      data /senml:e/s
60010      data /senml:e/t
60011      data /senml:e/u
60012      data /senml:e/ut
60013      data /senml:e/v
60014      data /senml:e/vb
60015      data /senml:e/vd
60016      data /senml:e/vs

File senml@unknown.sid created
Number of SIDs available : 100
Number of SIDs used : 17
~~~~

However, we can modify the SIDs manually so that the resultant CORECONF will have deltas conforming to SenML-CBOR Labels as defined in section 12.2 of {{RFC8428}}:

~~~~
SID        Assigned to
---------  --------------------------------------------------
60010      module senml
60000      data /senml:e
59998      data /senml:e/bn
59994      data /senml:e/bs
59997      data /senml:e/bt
59996      data /senml:e/bu
59995      data /senml:e/bv
59999      data /senml:e/bver
60000      data /senml:e/n
60005      data /senml:e/s
60006      data /senml:e/t
60001      data /senml:e/u
60007      data /senml:e/ut
60002      data /senml:e/v
60004      data /senml:e/vb
60008      data /senml:e/vd
60003      data /senml:e/vs
~~~~

The CORECONF diagnostic format of the data instance is shown below:

~~~~
{60000: [{-3: 1.001,
          -2: 'urn:dev:ow:10e2073a0108006:',
          0: 'temperature',
          1: 'Cel',
          2: 23.1,
          6: 1},
         {0: 'humidity',
          1: '%RH',
          2: 67.3,
          6: 2}]
}
~~~~

The above CORECONF list conforms to SenML CBOR specification and can be easily parsed by SenML parsers. Also, it is represented in CBOR encoded hexadecimal digits as follows:

~~~~
CBOR Hex:

a119ea6082a621781b75726e3a6465763a6f773a3130653230373361303130383030363a22fb3ff004189374bc6a006b74656d7065726174757265016343656c02fb403719999999999a0601a4006868756d6964697479016325524802fb4050d333333333330602
~~~~

Finally, a simple comparison of the JSON with the corresponding CORECONF-CBOR encoded form is shown below:

|---
| Module Name | JSON Size | CORECONF Size | Compression %
|-|- |-|-
| Present | 140 Bytes |  104 Bytes | 25.71
| Absent  | 121 Bytes | 100 Bytes  | 17.36
|===


# Further work

Three primary areas of future work have been identified to improve SenML YANG modelling- 

1. Base units can be either modelled as enumerated type or identityref type, so they can be assigned a SID value. This should ideally further reduce the CORECONF-CBOR encoded message.
2. Constraints on having leaves v, vs, vb, vd optional if s is available as described in Section 4.2 of {{RFC8428}}
3. Add secondary units described in {{RFC8798}} in the base units constraints.
4. SIDs for /senml:e/n and /senml:e have to be identical in order for CORECONF to correctly have 0 as CBOR Label for the name field. This in theory breaks uniqueness of the schema identifiers, however it won't affect the data encoding or decoding.


