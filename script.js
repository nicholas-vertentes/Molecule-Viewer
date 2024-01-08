$(document).ready(
    function () {
        $("#addElementButton").click(
            function () {
                $.post("/addElement_handler.html",
                    {
                        Element_Number: $("#enterElementNumber").val(),
                        Element_Code: $("#enterElementCode").val(),
                        Element_Name: $("#enterElementName").val(),
                        Colour1: $("#enterColour1").val(),
                        Colour2: $("#enterColour2").val(),
                        Colour3: $("#enterColour3").val(),
                        Element_Radius: $("#enterElementRadius").val(),
                    },
                    function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    }
                );
            }
        );

        $("#removeElementButton").click(
            function () {
                $.post("/removeElement_handler.html",
                    {
                        Element_Code: $("#removeElementCode").val(),
                    },
                    function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    },
                );
            },   
        );

        // $("#moleculeUploadContinueButton").click(
        //     function () {
        //         $.post("/uploadSDF.html");
        //     }
        // );

        $("#xyz-rotationButton").click(
            function () {
                $.post("/xyz-rotation_handler.html",
                    {
                        X_Rotation: $("#x-rotationText").val() || 0,
                        Y_Rotation: $("#y-rotationText").val() || 0,
                        Z_Rotation: $("#z-rotationText").val() || 0,
                        Molecule_Name: $("#rotationMoleculeName").text(),
                    },
                    function (data) {
                        $("#svg_box").html(data);
                    },
                );
            },
        );

        $("#resetRotationButton").click(
            function () {
                $.post("/resetRotation_handler.html",
                    {
                        Molecule_Name: $("#rotationMoleculeName").text(),
                    },
                    function (data) {
                        $("#svg_box").html(data);
                    },
                );
            },
        );
    }
);