let riskData = {};


/* =========================
   LOAD RISK DATA
========================= */

fetch("risk_data.json")
    .then(response => response.json())
    .then(data => {

        data.forEach(item => {

            riskData[item.municipio] = item;

        });

        loadMap();

    });


/* =========================
   MAP CONFIGURATION
========================= */

const map = L.map('map', {

    scrollWheelZoom: false,

    dragging: false,

    doubleClickZoom: false,

    boxZoom: false,

    keyboard: false,

    zoomControl: false,

    touchZoom: false

});


/* =========================
   LOAD MAP
========================= */

function loadMap() {

    fetch("Jalisco.json")
        .then(response => response.json())
        .then(data => {

            const geojsonLayer = L.geoJSON(data, {

                style: function(feature) {

                    const municipio =
                        feature.properties.NOMGEO;

                    const municipalityData =
                        riskData[municipio];

                    const risk =
                        municipalityData?.predicted_pd;

                    return {

                        color: "#343333",

                        weight: 1,

                        fillColor: getColor(risk),

                        fillOpacity: 0.8
                    };
                },

                onEachFeature: function(feature, layer) {

                    const municipalityCard =
                        document.getElementById("municipality-card");

                    const municipalityName =
                        document.getElementById("municipality-name");

                    const municipalityPD =
                        document.getElementById("municipality-pd");

                    const municipalityEL =
                        document.getElementById("municipality-el");

                    const municipalityApproval =
                        document.getElementById("municipality-approval");


                    layer.on({

                        mouseover: function(e) {

                            const municipio =
                                feature.properties.NOMGEO;

                            const municipalityData =
                                riskData[municipio];


                            municipalityName.textContent =
                                municipio;


                            if (municipalityData) {

                                municipalityPD.textContent =
                                    `${(municipalityData.predicted_pd * 100).toFixed(2)}%`;

                                municipalityEL.textContent =
                                    `$${municipalityData.expected_loss.toLocaleString()}`;

                                municipalityApproval.textContent =
                                    `${(municipalityData.approval_rate * 100).toFixed(0)}%`;

                            }

                            else {

                                municipalityPD.textContent =
                                    "NO DATA";

                                municipalityEL.textContent =
                                    "NO DATA";

                                municipalityApproval.textContent =
                                    "NO DATA";
                            }


                            municipalityCard.classList.add("active");


                            e.target.setStyle({

                                fillColor: "#8B0000",

                                fillOpacity: 1
                            });

                        },


                        mouseout: function(e) {

                            municipalityCard.classList.remove("active");

                            const municipio =
                                feature.properties.NOMGEO;

                            const municipalityData =
                                riskData[municipio];

                            const risk =
                                municipalityData?.predicted_pd;


                            e.target.setStyle({

                                fillColor: getColor(risk),

                                fillOpacity: 0.8
                            });

                        }

                    });

                }

            }).addTo(map);


            map.fitBounds(
                geojsonLayer.getBounds()
            );

            map.zoomIn(0.3);

            map.panBy([0, 10]);

        });

}


/* =========================
   RISK COLORS
========================= */

function getColor(risk) {

    if (risk == null)
        return "#4f4f4f";

    if (risk >= 0.65) /* This is the threshold for very high risk */
        return "#4a0404";

    if (risk >= 0.50) /* This is the threshold for high risk */
        return "#8B0000";

    if (risk >= 0.35) /* This is the threshold for moderate risk */
        return "#ce6f02";

    if (risk >= 0.22) /* This is the threshold for low risk */
        return "#146a15";

    return "#3f634b";
}

/* =========================
   SCROLL ANIMATION
========================= */

const heroContent =
    document.querySelector(".hero-content");


window.addEventListener("scroll", () => {

    const scrollY = window.scrollY;

    const opacity =
        1 - scrollY / 50;

    heroContent.style.opacity =
        Math.max(opacity, 0);


    heroContent.style.transform =
        `translateY(calc(-50% - ${scrollY * 0.2}px))`;

});