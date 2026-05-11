let riskData = {};
let dashboardData = {};

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

                    const municipalityRisk =    
                    document.getElementById("municipality-risk");

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

                            if (municipalityData.risk_bucket === "Low") {

                                municipalityRisk.style.color = "#146a15";

                            }

                            else if (municipalityData.risk_bucket === "Medium") {

                                municipalityRisk.style.color = "#d6a700";

                            }

                            else if (municipalityData.risk_bucket === "High") {

                                municipalityRisk.style.color = "#8B0000";

                            }


                            if (municipalityData) {

                                municipalityPD.textContent =
                                    `${(municipalityData.predicted_pd * 100).toFixed(2)}%`;

                                municipalityEL.textContent =
                                    `$${municipalityData.expected_loss.toLocaleString()}`;

                                municipalityApproval.textContent =
                                    `${(municipalityData.approval_rate * 100).toFixed(0)}%`;
                                municipalityRisk.textContent =
                                    municipalityData.risk_bucket;
                            }

                            else {

                                municipalityPD.textContent =
                                    "NO DATA";

                                municipalityEL.textContent =
                                    "NO DATA";

                                municipalityApproval.textContent =
                                    "NO DATA";

                                municipalityRisk.textContent =
                                    "NO DATA";
                            }


                            municipalityCard.classList.add("active");


                            e.target.setStyle({

                                fillColor: "#155f97",

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
        return "#340000";

    if (risk >= 0.66) /* This is the threshold for very high risk */
        return "#4a0404";

    if (risk >= 0.36) /* This is the threshold for moderate risk */
        return "#ce6f02";

    if (risk >= 0.1) /* This is the threshold for low risk */
        return "#146a15";

    return "#580000";
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


fetch("dashboard_data.json")
    .then(response => response.json())
    .then(data => {

        dashboardData = data;

        loadDashboard();

    });

function loadDashboard() {

    const plotTheme = {
        paper_bgcolor: "rgba(239, 239, 239, 0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
            color: "#ffffff",
            family: "Poppins"
        },
        xaxis: {
            showgrid: false,
            zeroline: false,
        },
        yaxis: {
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.2)",
            zeroline: false
        }
    };


    /* =========================
       ROC TRAIN
    ========================= */

    Plotly.newPlot("roc-train", [{
        x: dashboardData.roc_train.fpr,
        y: dashboardData.roc_train.tpr,
        mode: "lines",
        name: "Train ROC",
        line: {
            color: "#ffffff",
            width: 4
        }
    },
    {
        x: [0,1],
        y: [0,1],
        mode: "lines",
        name: "Baseline",
        line: {
            color: "#de0000",
            dash: "dash"
        }
    }], {
        ...plotTheme,
        title: "ROC Curve - Train",
        autosize: true,
        height: 520
    });


    /* =========================
       ROC TEST
    ========================= */

    Plotly.newPlot("roc-test", [{
        x: dashboardData.roc_test.fpr,
        y: dashboardData.roc_test.tpr,
        mode: "lines",
        name: "Test ROC",
        line: {
            color: "#fffefe",
            width: 4
        }
    },
    {
        x: [0,1],
        y: [0,1],
        mode: "lines",
        name: "Baseline",
        line: {
            color: "#e20000",
            dash: "dash"
        }
    }], {
        ...plotTheme,
        title: "ROC Curve - Test",
        autosize: true,
        height: 520
    });

    const cmTrain = dashboardData.cm_train;

    Plotly.newPlot("cm-train", [{
        z: cmTrain,
        type: "heatmap",
        colorscale: [
            [0, "#d6d6d6"],
            [1, "#72946f"]
        ],
        showscale: false,
        hoverinfo: "skip"
    }], {
        ...plotTheme,

        title: "Confusion Matrix - Train",

        autosize: true,

        height: 700,

        annotations: [

            {
                x: 0,
                y: 0,
                text: `TN<br>${cmTrain[0][0]}`,
                showarrow: false,
                font: {
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 1,
                y: 0,
                text: `FP<br>${cmTrain[0][1]}`,
                showarrow: false,
                font: {
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 0,
                y: 1,
                text: `FN<br>${cmTrain[1][0]}`,
                showarrow: false,
                font: {
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 1,
                y: 1,
                text: `TP<br>${cmTrain[1][1]}`,
                showarrow: false,
                font: {
                    color: "#ae0000",
                    size: 24
                }
            }

        ],

        xaxis: {
            title: "Predicted Label",
            tickvals: [0, 1],
            ticktext: ["0", "1"],
            showgrid: false,
            zeroline: false
        },

        yaxis: {
            title: "True Label",
            tickvals: [0, 1],
            ticktext: ["0", "1"],
            autorange: "reversed",
            showgrid: false,
            zeroline: false
        }

    });



    const cmTest = dashboardData.cm_test;

    Plotly.newPlot("cm-test", [{
        z: cmTest,
        type: "heatmap",
        colorscale: [
            [0, "#d6d6d6"],
            [1, "#72946f"]
        ],
        showscale: false,
        hoverinfo: "skip"
    }], {
        ...plotTheme,

        title: "Confusion Matrix - Test",

        autosize: true,

        height: 700,

        annotations: [

            {
                x: 0,
                y: 0,
                text: `TN<br>${cmTest[0][0]}`,
                showarrow: false,
                font: {
                    font_family: "Poppins",
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 1,
                y: 0,
                text: `FP<br>${cmTest[0][1]}`,
                showarrow: false,
                font: {
                    font_family: "Poppins",
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 0,
                y: 1,
                text: `FN<br>${cmTest[1][0]}`,
                showarrow: false,
                font: {
                    font_family: "Poppins",
                    color: "#ae0000",
                    size: 24
                }
            },

            {
                x: 1,
                y: 1,
                text: `TP<br>${cmTest[1][1]}`,
                showarrow: false,
                font: {
                    font_family: "Poppins",
                    color: "#ae0000",
                    size: 24
                }
            }

        ],

        xaxis: {
            title: "Predicted Label",
            tickvals: [0, 1],
            ticktext: ["0", "1"],
            showgrid: false,
            zeroline: false
        },

        yaxis: {
            title: "True Label",
            tickvals: [0, 1],
            ticktext: ["0", "1"],
            autorange: "reversed",
            showgrid: false,
            zeroline: false
        }

    });
    /* =========================
   DENSITY TRAIN
========================= */

    Plotly.newPlot("density-train", [

        {
            x: dashboardData.density_train.approved_x,
            y: dashboardData.density_train.approved_y,
            mode: "lines",
            name: "Approved",
            line: {
                color: "#d6d6d6",
                width: 4,
                shape: "spline"
            },
            fill: "tozeroy",
            fillcolor: "rgba(214,214,214,0.28)"
        },

        {
            x: dashboardData.density_train.denied_x,
            y: dashboardData.density_train.denied_y,
            mode: "lines",
            name: "Denied",
            line: {
                color: "#8B0000",
                width: 4,
                shape: "spline"
            },
            fill: "tozeroy",
            fillcolor: "rgba(139,0,0,0.28)"
        }

    ], {

        ...plotTheme,

        title: "Probability Density - Train",

        autosize: true,

        height: 520,

        xaxis: {
            ...plotTheme.xaxis,
            title: "Predicted Probability"
        },

        yaxis: {
            ...plotTheme.yaxis,
            title: "Density"
        }

    });


    /* =========================
    DENSITY TEST
    ========================= */

    Plotly.newPlot("density-test", [

        {
            x: dashboardData.density_test.approved_x,
            y: dashboardData.density_test.approved_y,
            mode: "lines",
            name: "Approved",
            line: {
                color: "#d6d6d6",
                width: 4,
                shape: "spline"
            },
            fill: "tozeroy",
            fillcolor: "rgba(214,214,214,0.28)"
        },

        {
            x: dashboardData.density_test.denied_x,
            y: dashboardData.density_test.denied_y,
            mode: "lines",
            name: "Denied",
            line: {
                color: "#8B0000",
                width: 4,
                shape: "spline"
            },
            fill: "tozeroy",
            fillcolor: "rgba(139,0,0,0.28)"
        }

    ], {

        ...plotTheme,

        title: "Probability Density - Test",

        autosize: true,

        height: 520,

        xaxis: {
            ...plotTheme.xaxis,
            title: "Predicted Probability"
        },

        yaxis: {
            ...plotTheme.yaxis,
            title: "Density"
        }

    });



    /* =========================
    RISK BUCKET 
    ========================= */
        

        Plotly.newPlot("risk-bucket-train", [{
        type: "violin",
        x: dashboardData.risk_bucket_train.labels,
        y: dashboardData.risk_bucket_train.values,
        points: false,
        box: {
            visible: true
        },
        meanline: {
            visible: true
        },
        line: {
            color: "#8e0606"
        },
        fillcolor: "rgba(134,134,134,0.45)"
    }], {
        ...plotTheme,
        title: "Risk Buckets - Train",
        autosize: true,
        height: 520,
        xaxis: {
            title: "Risk Bucket",
            showgrid: false,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        },
        yaxis: {
            title: "Predicted PD",
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        }
    });


    Plotly.newPlot("risk-bucket-test", [{
        type: "violin",
        x: dashboardData.risk_bucket_test.labels,
        y: dashboardData.risk_bucket_test.values,
        points: false,
        box: {
            visible: true
        },
        meanline: {
            visible: true
        },
        line: {
            color: "#8e0606"
        },
        fillcolor: "rgba(134,134,134,0.35)"
    }], {
        ...plotTheme,
        title: "Risk Buckets - Test",
        autosize: true,
        height: 520,
        xaxis: {
            title: "Risk Bucket",
            showgrid: false,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        },
        yaxis: {
            title: "Predicted PD",
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        }
    });

    Plotly.newPlot("interest-rate-train", [{
        type: "violin",
        x: dashboardData.interest_rate_train.labels,
        y: dashboardData.interest_rate_train.values,
        points: false,
        box: {
            visible: true
        },
        meanline: {
            visible: true
        },
        line: {
            color: "#8e0606"
        },
        fillcolor: "rgba(134,134,134,0.45)"
    }], {
        ...plotTheme,
        title: "Interest Rate by Risk Bucket - Train",
        autosize: true,
        height: 520,
        xaxis: {
            title: "Risk Bucket",
            showgrid: false,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        },
        yaxis: {
            title: "Interest Rate",
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        }
    });


    Plotly.newPlot("interest-rate-test", [{
        type: "violin",
        x: dashboardData.interest_rate_test.labels,
        y: dashboardData.interest_rate_test.values,
        points: false,
        box: {
            visible: true
        },
        meanline: {
            visible: true
        },
        line: {
            color: "#8e0606"
        },
        fillcolor: "rgba(134,134,134,0.35)"
    }], {
        ...plotTheme,
        title: "Interest Rate by Risk Bucket - Test",
        autosize: true,
        height: 520,
        xaxis: {
            title: "Risk Bucket",
            showgrid: false,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        },
        yaxis: {
            title: "Interest Rate",
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false
        }
    });

}