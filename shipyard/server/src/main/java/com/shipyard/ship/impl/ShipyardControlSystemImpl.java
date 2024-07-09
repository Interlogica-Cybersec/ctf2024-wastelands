package com.shipyard.ship.impl;

import com.shipyard.ship.shared.dto.Ship;
import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;

import java.util.List;

public class ShipyardControlSystemImpl implements ShipyardControlSystem {

    private static final String workingShipUuid = "3711cda7-0654-4677-ae84-782a4b6ebb9d";

    @Override
    public String getShipStartupKey(String shipId) {
        if (workingShipUuid.equals(shipId)) {
            return "NTRLGC{F1n4lly_th3r3_1s_h0p3!}";
        } else {
            return "Ship currently offline";
        }
    }

    @Override
    public List<Ship> getShips() {
        return List.of(
                new Ship(
                        "b094bc0f-f7a0-4682-8cf9-35f9206caba8",
                        "The Gargantuan",
                        "\"The Gargantuan\" is not just a yacht; it's a floating palace of opulence and luxury, a marvel of modern engineering and design. As you step on board, you're immediately enveloped in an atmosphere of extravagance and sophistication. \n" +
                                "\n" +
                                "Stretching over 40 meters in length, this majestic vessel commands attention with its sleek lines and imposing presence on the water. Its towering mast reaches towards the sky, adorned with billowing sails that catch the wind with effortless grace.\n" +
                                "\n" +
                                "Step inside, and you'll find yourself transported to a world of unparalleled luxury. The interior is a symphony of sumptuous materials and exquisite craftsmanship, with every detail meticulously curated to indulge the senses.\n" +
                                "\n" +
                                "From the grand ballroom, where crystal chandeliers cast a soft, golden glow over polished marble floors, to the private suites, each more lavish than the last, \"The Gargantuan\" offers a sanctuary of indulgence for its discerning guests.\n" +
                                "\n" +
                                "On deck, a sprawling sun deck beckons with plush loungers and a shimmering infinity pool, offering panoramic views of the endless horizon. For those seeking adventure, a fleet of water toys and a helipad stand ready to whisk you away on unforgettable excursions.\n" +
                                "\n" +
                                "\"The Gargantuan\" is not just a yacht; it's a symbol of wealth, power, and ultimate luxury, destined to leave an impression wherever it sails.",
                        false,
                        "last contact: 50 years ago",
                        "/assets/ships/the-gargantuan.jpeg"
                ),
                new Ship(
                        workingShipUuid,
                        "The Tub",
                        "\"The Tub\" may be modest in size, but it's big on character and charm. This humble fishing vessel may not boast the grandeur of a luxury yacht, but what it lacks in size, it more than makes up for in character and functionality.\n" +
                                "\n" +
                                "Measuring just 10 meters from bow to stern, \"The Tub\" is a sturdy and reliable vessel designed for the discerning angler. Its weathered hull bears the marks of countless voyages, a testament to its years of service on the open sea.\n" +
                                "\n" +
                                "Step on board, and you're greeted by the salty tang of the ocean and the reassuring hum of the engine. The deck is cluttered with nets, crates, and tackle boxes, each item a vital tool in the pursuit of the day's catch.\n" +
                                "\n" +
                                "In the cramped but cozy cabin, you'll find all the comforts of home, albeit on a smaller scale. A simple galley offers the means to cook up the day's fresh catch, while a snug sleeping berth provides a place to rest weary bones after a long day at sea.\n" +
                                "\n" +
                                "\"The Tub\" may not be the most glamorous vessel on the water, but it's beloved by its crew for its reliability and seaworthiness. Whether navigating treacherous waters or casting lines in search of the perfect catch, \"The Tub\" is always ready for adventure, proving that you don't need size to make a big splash on the high seas.",
                        true,
                        null,
                        "/assets/ships/the-tub.jpeg"),
                new Ship(
                        "4dfac0cc-aa50-4000-a2f8-bc3fc053cf67",
                        "The Formidable",
                        "\"The Formidable\" epitomizes elegance and sophistication on the high seas. This extraordinary yacht is a blend of classic design and modern innovation, exuding an aura of timeless luxury.\n" +
                                "\n" +
                                "Measuring 38 meters from bow to stern, \"The Formidable\" cuts through the waves with grace and precision, its sleek hull gliding effortlessly through the water. Its striking profile commands attention, with clean lines and a bold silhouette that speak to its strength and power.\n" +
                                "\n" +
                                "Step on board, and you're greeted by an atmosphere of refined luxury. The interior is a masterful blend of rich woods, polished metals, and sumptuous fabrics, creating a sense of warmth and comfort throughout.\n" +
                                "\n" +
                                "From the spacious salon, where plush sofas invite you to relax and unwind, to the stately dining room, set for lavish meals prepared by a world-class chef, every space on \"The Formidable\" is designed with the utmost attention to detail.\n" +
                                "\n" +
                                "On deck, a world of adventure awaits. A sun-drenched pool deck offers the perfect spot for soaking up the sun, while a fully equipped gym and spa provide opportunities for relaxation and rejuvenation. For those seeking thrills, a fleet of water toys stands ready for exploration and excitement.\n" +
                                "\n" +
                                "\"The Formidable\" is not just a yacht; it's a symbol of prestige and refinement, a sanctuary of luxury on the open ocean. Whether cruising crystal-clear waters or hosting extravagant soirées under the stars, this magnificent vessel promises an unforgettable experience for all who step on board.",
                        false,
                        "last contact: 50 years ago",
                        "/assets/ships/the-formidable.jpeg"),
                new Ship(
                        "4d02990f-0cc4-4b93-938e-97b4570066fd",
                        "The Magnificent",
                        "\"The Magnificent\" may be diminutive in size, but its name speaks volumes about the experiences it offers. This charming yacht, measuring a modest 27 meters from bow to stern, embodies a world of adventure and relaxation on the water.\n" +
                                "\n" +
                                "With its sleek lines and gleaming hull, \"The Magnificent\" cuts a graceful figure as it glides through the waves. Its compact size allows for nimble maneuvering, perfect for exploring hidden coves and secluded beaches unreachable by larger vessels.\n" +
                                "\n" +
                                "Step on board, and you'll discover a world of comfort and style in a compact package. The deck is adorned with plush cushions and sun loungers, inviting you to soak up the sun and enjoy the gentle sea breeze.\n" +
                                "\n" +
                                "Below deck, the cabin is cozy yet well-appointed, with a compact galley and sleeping quarters designed for maximum comfort. Rich wood finishes and soft lighting create an ambiance of warmth and relaxation, making it the perfect retreat after a day of sailing.\n" +
                                "\n" +
                                "Despite its small size, \"The Magnificent\" is equipped with all the amenities needed for a memorable voyage. A well-stocked bar ensures that refreshments are never far away, while a selection of water toys provides endless opportunities for fun and adventure on the water.\n" +
                                "\n" +
                                "\"The Magnificent\" may be small in stature, but it offers a world of luxury and excitement for those seeking a unique and unforgettable yachting experience.",
                        false,
                        "last contact: 50 years ago",
                        "/assets/ships/the-magnificent.jpeg"),
                new Ship("b0f6b469-6609-48da-9748-e2f433ed1761",
                        "The Fabled",
                        "\"The Fabled\" is a yacht that whispers tales of adventure and mystery, embodying the allure of the open sea and the enchantment of distant lands. This vessel, though modest in size at 24 meters, exudes an undeniable charm and charisma that captivates all who come aboard.\n" +
                                "\n" +
                                "With its elegant lines and polished exterior, \"The Fabled\" commands attention wherever it sails. Its sleek profile cuts through the water with grace and ease, while its sturdy hull ensures a smooth and comfortable ride even in choppy seas.\n" +
                                "\n" +
                                "Step on board, and you'll be transported to a world of wonder and excitement. The deck is a playground of possibilities, with ample space for lounging in the sun or dining al fresco under the stars. Aft, a cozy seating area beckons with plush cushions and sweeping views of the horizon.\n" +
                                "\n" +
                                "Below deck, the cabin is a haven of comfort and luxury. Rich wood finishes and soft lighting create an atmosphere of warmth and tranquility, while thoughtful design touches ensure that every inch of space is maximized for comfort and convenience.\n" +
                                "\n" +
                                "Congratulations Wastelands survivor, you are one of the few who read everything. Nice catch hehe.\n" +
                                "\n" +
                                "Despite its modest size, \"The Fabled\" is equipped with all the amenities needed for a memorable voyage. A well-appointed galley allows for gourmet meals to be prepared with ease, while a selection of water toys and recreational equipment ensures that there's never a dull moment on board.\n" +
                                "\n" +
                                "\"The Fabled\" may be small in size, but it offers an experience that is truly larger than life. With its sense of adventure and spirit of exploration, this enchanting yacht promises to make every journey an unforgettable tale to be told for years to come.",
                        false,
                        "last contact: 50 years ago",
                        "/assets/ships/the-fabled.jpeg"),
                new Ship("77a03bfd-a6b3-4977-82e3-6774f551affd",
                        "The Unsinkable III",
                        "\"The Unsinkable III\" rises like a phoenix from the waves, a testament to resilience and unwavering determination. This medium-sized sailboat, measuring 32 meters in length, carries the legacy of its predecessors, \"The Unsinkable I\" and \"The Unsinkable II,\" which met unfortunate fates beneath the sea's surface.\n" +
                                "\n" +
                                "Despite its predecessors' misfortunes, \"The Unsinkable III\" sails with renewed purpose and strength. Its robust hull is reinforced with the latest in marine engineering technology, ensuring unparalleled durability and safety on the open water.\n" +
                                "\n" +
                                "Step on board, and you'll find a vessel that is as practical as it is resilient. The deck is spacious and well-appointed, with ample seating for guests to relax and enjoy the salty sea breeze. Aft, a sleek cockpit offers commanding views of the horizon, with state-of-the-art navigation equipment at the ready.\n" +
                                "\n" +
                                "Below deck, the cabin is a cozy retreat from the elements, with comfortable sleeping quarters and a compact galley for preparing meals. Despite its modest size, every inch of space is carefully utilized to maximize comfort and functionality.\n" +
                                "\n" +
                                "\"The Unsinkable III\" may bear the weight of its predecessors' legacies, but it sails with confidence and optimism towards new horizons. With its unwavering commitment to safety and reliability, this resilient sailboat promises to defy the odds and chart a course towards a brighter future on the open sea.",
                        false,
                        "sank upon inauguration",
                        "/assets/ships/the-unsinkable.jpeg")
        );
    }

    @Override
    public String pingShipTransponder(String shipId) {
        if (workingShipUuid.equals(shipId)) {
            return "Ping successful";
        } else {
            return "Ping failed - transponder offline";
        }
    }

    @Override
    public String reserveShip(String shipId) {
        return "Error - reason unknown";
    }

    @Override
    public String scheduleForMaintenance(String shipId) {
        return "Error - reason unknown";
    }

    @Override
    public String getReservationHistory(String shipId) {
        return "Error - reason unknown";
    }

    @Override
    public String getAdditionalInformation(String shipId) {
        return "Error - reason unknown";
    }
}
