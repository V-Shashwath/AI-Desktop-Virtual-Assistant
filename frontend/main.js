$(document).ready(function () {

    // Authentication Choice Button Handlers
    $("#FaceAuthBtn").click(function () {
        eel.chooseFaceAuth()();
    });

    $("#PasscodeAuthBtn").click(function () {
        eel.choosePasscodeAuth()();
    });

    // Passcode Input Handling
    $(".passcode-digit").on("input", function() {
        const value = $(this).val();
        // Only allow numbers
        if (!/^\d$/.test(value)) {
            $(this).val("");
            return;
        }
        
        $(this).addClass("filled");
        
        // Auto-focus next input
        const $inputs = $(".passcode-digit");
        const currentIndex = $inputs.index(this);
        if (currentIndex < $inputs.length - 1 && value) {
            $inputs.eq(currentIndex + 1).focus();
        }
    });

    // Handle backspace to go to previous input
    $(".passcode-digit").on("keydown", function(e) {
        if (e.key === "Backspace" && !$(this).val()) {
            const $inputs = $(".passcode-digit");
            const currentIndex = $inputs.index(this);
            if (currentIndex > 0) {
                $inputs.eq(currentIndex - 1).focus().val("").removeClass("filled");
            }
        }
    });

    // Verify Passcode Button
    $("#VerifyPasscodeBtn").click(function () {
        const passcode = $(".passcode-digit").map(function() {
            return $(this).val();
        }).get().join("");
        
        if (passcode.length === 6) {
            eel.verifyPasscode(passcode)();
        } else {
            $("#PasscodeError").text("Please enter all 6 digits").show();
            setTimeout(function() {
                $("#PasscodeError").hide();
            }, 3000);
        }
    });

    // Allow Enter key to verify passcode
    $(".passcode-digit").on("keypress", function(e) {
        if (e.which === 13) {
            $("#VerifyPasscodeBtn").click();
        }
    });

    eel.init()()

    $('.text').textillate({
        // loop: true,
        loop: false,
        in: {
            effect: 'fadeIn',
            sync: false 
        },
        out: {
            effect: 'fadeOut',
            sync: true 
        }
    });

    //siri-config
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style:"ios9",
        amplitude: 1,
        speed: "0.30",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        // loop: true,
        loop: false,
        in: {
            effect: 'fadeIn',
            sync: false 
        },
        out: {
            effect: 'fadeOut',
            sync: true 
        }
    });

    // Mic Button Click Event
    $('#MicBtn').click(function () {
        eel.playAssistantSound();
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    //shortcut key
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // play assistant
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }
    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message)
    });

    // send button event handler
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val()
        PlayAssistant(message)
    });

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });
    
    // ===== BACKGROUND BUTTON ===== 
    let backgroundActive = false;
    
    $('#BackgroundBtn').click(function () {
        $(this).addClass('button-click-effect');
        setTimeout(() => $(this).removeClass('button-click-effect'), 300);
        
        eel.toggleBackgroundListener()(function(status) {
            backgroundActive = status;
            
            if (status) {
                $('#BackgroundBtn')
                    .removeClass('btn-glow-green')
                    .addClass('btn-glow-red');
                
                $('#BackgroundStatus')
                    .text('Background Mode: ACTIVE')
                    .css('color', '#ff0000')
                    .addClass('active');
                
                swal({
                    title: "🎤 Background Mode Activated!",
                    text: "Say 'Hey Computer' to wake me up!",
                    icon: "success",
                    button: "Got it!"
                });
            } else {
                $('#BackgroundBtn')
                    .removeClass('btn-glow-red')
                    .addClass('btn-glow-green');
                
                $('#BackgroundStatus')
                    .text('Background Mode: OFF')
                    .css('color', '#00ff00')
                    .removeClass('active');
                
                swal({
                    title: "👤 Background Mode Deactivated",
                    text: "Background listening has been stopped.",
                    icon: "info",
                    button: "OK"
                });
            }
        });
    });
    
    // Settings Code

    eel.personalInfo()();
    eel.displaySysCommand()();
    eel.displayWebCommand()();
    eel.displayPhoneBookCommand()();



    // Execute: python side :
    eel.expose(getData)
    function getData(user_info) {
        let data = JSON.parse(user_info);
        let idsPersonalInfo = ['OwnerName', 'Mobile', 'Email', 'City']
        let idsInputInfo = ['InputOwnerName', 'InputMobile', 'InputEmail', 'InputCity']

        for (let i = 0; i < data.length; i++) {
            hashid = "#" + idsPersonalInfo[i]
            $(hashid).text(data[i]);
            $("#" + idsInputInfo[i]).val(data[i]);
        }

    }

    // Personal Data Update Button:

    $("#UpdateBtn").click(function () {

        let OwnerName = $("#InputOwnerName").val();
        let Mobile = $("#InputMobile").val();
        let Email = $("#InputEmail").val();
        let City = $("#InputCity").val();

        if (OwnerName.length > 0 && Mobile.length > 0 && Email.length > 0 && City.length > 0) {
            eel.updatePersonalInfo(OwnerName, Mobile, Email, City)

            swal({
                title: "Updated Successfully",
                icon: "success",
            });


        }
        else {
            const toastLiveExample = document.getElementById('liveToast')
            const toast = new bootstrap.Toast(toastLiveExample)

            $("#ToastMessage").text("All Fields Mandatory");

            toast.show()
        }

    });


    // Display System Command Method
    eel.expose(displaySysCommand)
    function displaySysCommand(array) {

        let data = JSON.parse(array);
        console.log(data)

        let placeholder = document.querySelector("#TableData");
        let out = "";
        let index = 0
        for (let i = 0; i < data.length; i++) {
            index++
            out += `
                    <tr>
                        <td class="text-light"> ${index} </td>
                        <td class="text-light"> ${data[i][1]} </td>
                        <td class="text-light"> ${data[i][2]} </td>
                        <td class="text-light"> <button id="${data[i][0]}" onClick="SysDeleteID(this.id)" class="btn btn-sm btn-glow-red">Delete</button></td>
                        
                    </tr>
            `;

            // console.log(data[i][0])
            // console.log(data[i][1])


        }

        placeholder.innerHTML = out;

    }

    // Add System Command Button
    $("#SysCommandAddBtn").click(function () {

        let key = $("#SysCommandKey").val();
        let value = $("#SysCommandValue").val();

        if (key.length > 0 && value.length) {
            eel.addSysCommand(key, value)

            swal({
                title: "Updated Successfully",
                icon: "success",
            });
            eel.displaySysCommand()();
            $("#SysCommandKey").val("");
            $("#SysCommandValue").val("");


        }
        else {
            const toastLiveExample = document.getElementById('liveToast')
            const toast = new bootstrap.Toast(toastLiveExample)

            $("#ToastMessage").text("All Fields Medatory");

            toast.show()
        }

    });


    // Display Web Commands Table
    eel.expose(displayWebCommand)
    function displayWebCommand(array) {

        let data = JSON.parse(array);
        console.log(data)

        let placeholder = document.querySelector("#WebTableData");
        let out = "";
        let index = 0
        for (let i = 0; i < data.length; i++) {
            index++
            out += `
                    <tr>
                        <td class="text-light"> ${index} </td>
                        <td class="text-light"> ${data[i][1]} </td>
                        <td class="text-light"> ${data[i][2]} </td>
                        <td class="text-light"> <button id="${data[i][0]}" onClick="WebDeleteID(this.id)" class="btn btn-sm btn-glow-red">Delete</button></td>
                        
                    </tr>
            `;

            // console.log(data[i][0])
            // console.log(data[i][1])


        }

        placeholder.innerHTML = out;

    }


    // Add Web Commands

    $("#WebCommandAddBtn").click(function () {

        let key = $("#WebCommandKey").val();
        let value = $("#WebCommandValue").val();

        if (key.length > 0 && value.length) {
            eel.addWebCommand(key, value)

            swal({
                title: "Updated Successfully",
                icon: "success",
            });
            eel.displayWebCommand()();
            $("#WebCommandKey").val("");
            $("#WebCommandValue").val("");


        }
        else {
            const toastLiveExample = document.getElementById('liveToast')
            const toast = new bootstrap.Toast(toastLiveExample)

            $("#ToastMessage").text("All Fields Medatory");

            toast.show()
        }

    });


    // Display Phone Book

    eel.expose(displayPhoneBookCommand)
    function displayPhoneBookCommand(array) {

        let data = JSON.parse(array);
        console.log(data)

        let placeholder = document.querySelector("#ContactTableData");
        let out = "";
        let index = 0
        for (let i = 0; i < data.length; i++) {
            index++
            out += `
                    <tr>
                        <td class="text-light"> ${index} </td>
                        <td class="text-light"> ${data[i][1]} </td>
                        <td class="text-light"> ${data[i][2]} </td>
                        <td class="text-light"> ${data[i][3]} </td>
                        <td class="text-light"> ${data[i][4]} </td>
                        <td class="text-light"> <button id="${data[i][0]}" onClick="ContactDeleteID(this.id)" class="btn btn-sm btn-glow-red">Delete</button></td>
                        
                    </tr>
            `;


        }

        placeholder.innerHTML = out;

    }

    // Add Contacts to database

    $("#AddContactBtn").click(function () {

        let Name = $("#InputContactName").val();
        let MobileNo = $("#InputContactMobileNo").val();
        let Email = $("#InputContactEmail").val();
        let City = $("#InputContactCity").val();

        if (Name.length > 0 && MobileNo.length > 0) {

            if (Email.length < 0) {
                Email = "";
            }
            else if (City < 0) {
                City = "";
            }

            eel.InsertContacts(Name, MobileNo, Email, City)

            swal({
                title: "Updated Successfully",
                icon: "success",
            });

            $("#InputContactName").val("");
            $("#InputContactMobileNo").val("");
            $("#InputContactEmail").val("");
            $("#InputContactCity").val("");
            eel.displayPhoneBookCommand()()

        }
        else {
            const toastLiveExample = document.getElementById('liveToast')
            const toast = new bootstrap.Toast(toastLiveExample)

            $("#ToastMessage").text("Name and Mobile number Mandatory");

            toast.show()
        }

    });


});

function SysDeleteID(clicked_id) {


    // console.log(clicked_id);
    eel.deleteSysCommand(clicked_id)
    eel.displaySysCommand()();

}

function WebDeleteID(clicked_id) {


    // console.log(clicked_id);
    eel.deleteWebCommand(clicked_id)
    eel.displayWebCommand()();


}
function ContactDeleteID(clicked_id) {

    // console.log(clicked_id);
    eel.deletePhoneBookCommand(clicked_id)
    eel.displayPhoneBookCommand()();

}