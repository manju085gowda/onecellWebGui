/*	$(function () {

			$('#configreset').click(function(){
				$('#questionform')[0].reset();
			});

		});*/
          $(document).ready(function(){
            $('#upload-btn').prop('disabled',true);
            $("#question5").hide();
            $("#id_bc_ptp_port_1").prop("disabled", true);
            $("#id_bc_hems_communication_0").prop("disabled", true);
            $("#id_bc_hems_communication_1").prop("disabled", true);
            $("#id_bc_ca_communication_0").prop("disabled", true);
            $("#id_bc_ca_communication_1").prop("disabled", true);
            $('#guidata').DataTable();
	        $('#guidata1').DataTable();
	        $('#guidata2').DataTable();
            //$('#mgmtporterror').hide();

            /*$('#loginForm').validate("signin/",
                {
                    type: 'p',
                    fields: false,
                    event: 'submit',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        console.log("hey")
                    }
                    },
                    fieldInvalidCallback: function(field) {

                    }
                }
            );*/
            //$('#ipformclone').hide();


                   initvalidation();

            var $qForm = $('#questionform');
            $qForm.on('change',function(event){
                event.preventDefault()
                var $formData = $qForm.serialize()
                $.ajax({
                    type: "POST",
                    url: '/deployment_quessionnaire/',
                    data: $formData,
                    success: handleQuestionForm,
                })
            });

            function handleQuestionForm(data, textStatus, jqXHR){
				if ($("#id_bc_timing_1").is(":checked")) {
					$("#question5").show();
					//$('#bclock').show();

				} else {
					 $("#question5").hide();
					 $('#bclock').hide();

				}
				if($('#id_bc_ptp_port_1').is(":checked"))
                {
                  //$("#id_bc_ptp_port_1").prop("checked",false);
                 // $("#id_bc_ptp_port_0").prop("checked",true);
                /* $('#bclock').hide();
                 var bclock =  $('#bcDiv')
                 $('#backhaulDiv').append(bclock)*/
                }
                else
                {
                    //$("#id_bc_ptp_port_0").prop("checked",true);
                }

                /*if($('#id_bc_ca_communication_3').is(':checked'))
                {
                   $('#caserversection').hide();
                }
                else
                {
                  $('#caserversection').show();
                }*/


				/*if ($("#id_bc_mme_communication_1").is(":checked")) {
					$("#id_bc_hems_communication_0").prop("disabled", true);
					$("#id_bc_hems_communication_1").prop("disabled", true);
					$("#id_bc_hems_communication_2").prop("checked",true);
					$("#id_bc_ca_communication_0").prop("disabled", true);
					$("#id_bc_ca_communication_1").prop("disabled", true);
					*//*$("#id_bc_ca_communication_2").prop("checked",true);*//*
				} else {
					$("#id_bc_hems_communication_0").prop("disabled", false);
					$("#id_bc_hems_communication_1").prop("disabled", false);
				}

				if ($("#id_bc_hems_communication_0").is(":checked")) {
					$("#id_bc_ca_communication_0").prop("disabled", false);
					$("#id_bc_ca_communication_2").prop("disabled", false);
					$("#id_bc_ca_communication_1").prop("disabled", true);
				}
				if($("#id_bc_hems_communication_2").is(":checked")) {
					$("#id_bc_ca_communication_0").prop("disabled", false);
					$("#id_bc_ca_communication_1").prop("disabled", true);
					$("#id_bc_ca_communication_2").prop("disabled", false);
				}
				if($("#id_bc_hems_communication_1").is(":checked")) {
					$("#id_bc_ca_communication_0").prop("disabled", true);
					$("#id_bc_ca_communication_2").prop("disabled", false);
					$("#id_bc_ca_communication_1").prop("disabled", false);
					$("#id_bc_ptp_port_1").prop("disabled", false);
				}
				else
                {
                    $("#id_bc_ptp_port_1").prop("disabled", true);
                }*/

            }




        });

         $(function() {

          $(document).on('change', ':file', function() {
            var input = $(this),
                numFiles = input.get(0).files ? input.get(0).files.length : 1,
                label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
            input.trigger('fileselect', [numFiles, label]);
            $('#upload-btn').prop('disabled',false);
          });

          $(document).ready( function() {
              $(':file').on('fileselect', function(event, numFiles, label) {

                  var input = $(this).parents('.input-group').find(':text'),
                      log = numFiles > 1 ? numFiles + ' files selected' : label;

                  if( input.length ) {
                      input.val(log);
                  } else {
                      if( log ) alert(log);
                  }
                     $('#upload-btn').prop('disabled',false);
              });
          });

        });




        $('#form_fileupload').submit(function(event){
                event.preventDefault()
                var formData = new FormData($(this)[0]);
                $.ajax({
                        url: '/upload/',
                        type: 'POST',
                        data: formData,
                        async: true,
                        beforeSend: function() {
                            $("#loading-image").show();
                            $("#upload_status").hide();
                        },
                        success: function (data) {
                        console.log(data)
                        console.log(data.result)
                        console.log(data.response_data)
                        //var status_color = document.getElementById("upload_status")
                        if (data.status != "error")
                        {
                            console.log("success");
                            $("#upload_status").removeClass("alert-danger").addClass("alert-success");
                            $("#loading-image").hide();
                            $("#upload_status").html(data.result)
                            $("#upload_status").show();
                            $('#mgmtDiv').html(data.form_mgmt_html);
                            $('#backhaulDiv').html(data.form_backhaul_html);
                            $('#bcDiv').html(data.form_bc_html);
                            $('#fronthaulDiv').html(data.form_fronthaul_html);
                            $('#rdncyDiv').html(data.form_rdncy_html);
                            $('#hemsDiv').html(data.form_hems_html);
                            $('#caserverDiv').html(data.form_caserver_html);
                            $('#rootcertDiv').html(data.root_certificate_html);
                            $('#snmpDiv').html(data.form_snmp_html);
                            $('#whitelistDiv').html(data.form_whitelist_html);
                            $('#licenseDiv').html(data.form_license_html);
                            $('#leftnavigation').html(data.navigation_html);
                            $('#leftnavigation').attr('style', 'padding: 0px !important');
                            $('#file_upload_step').addClass('step_success');
                            initvalidation();
                        }
                        else
                        {
                            $("#upload_status").removeClass("alert-success").addClass("alert-danger");
                            $("#loading-image").hide();
                            $("#upload_status").html(data.result)
                            $("#upload_status").show();
                        }
                        },
                        error: function (data) {
                        console.log(data)
                        console.log("error")
                        $("#upload_status").html(data.result)
                        $("#upload_status").show();
                        $('#file_upload_step').removeClass('step_success');
                        $('#file_upload_step').removeClass('step_error');
                        },
                        cache: false,
                        contentType: false,
                        processData: false
                });
                return false;
        });


        function initvalidation()
        {
        /*$.autotab({ tabOnSelect: true });
        $(':input').autotab();
        $('.ipvalue').autotab({maxlength: 3,format: 'number'});
        $('.subnet').autotab({maxlength: 2,format: 'number'});
        $('.autotab4_fronthaul').autotab({maxlength: 4,format: 'number'});
        $('.autotab3_fronthaul').autotab({maxlength: 3,format: 'number'});
*/
           /* if($(this).is(":checked"))
           {
                $('#redundancyForm').find('div.webgui-configuration').show();
           }
           else
           {
                $('#redundancyForm').find('div.webgui-configuration').hide();
           }*/

           //initWizardNav();

            if($('#id_BCRedundancy').is(":checked"))
           {
                $('#redundancyForm').find('div.webgui-configuration').show();
           }
           else
           {
                $('#redundancyForm').find('div.webgui-configuration').hide();
           }
        $('#id_BCRedundancy').on('change', function()
        {
           if($(this).is(":checked"))
           {
                $('#redundancyForm').find('div.webgui-configuration').show();
           }
           else
           {
                $('#redundancyForm').find('div.webgui-configuration').hide();
           }
        });

        toggleMode();

        $('#SecGW1AddressType').on('change', function() {
                if(this.value.toLowerCase() == 'dynamic')
                {
                    $('#backhaulS1Gateway').children('div.static').hide();
                }
                else {
                    $('#backhaulS1Gateway').find('div.static').show();
                }
            });

            $('#SecGW2AddressType').on('change', function() {
                if(this.value.toLowerCase() == 'dynamic')
                {
                    $('#backhaulOAMGateway').children('div.static').hide();
                }
                else {
                    $('#backhaulOAMGateway').find('div.static').show();
                }
            });

            if($("#id_CUState_0").is(':checked'))
            {
                $('#vcellid').hide();
            }
             $('input[name="CUState"]').on('change', function() {
                if(this.value === 'Standby')
                {
                    $('#vcellid').hide();
                }
                else
                {
                  $('#vcellid').show();
                }
            });

            $("#mgmt-edit-btn" ).on( "click", function() {
              $( "li#nic" ).trigger( "click" );
            });

            $( "#snmp-edit-btn" ).on( "click", function() {
              $( "li#snmp" ).trigger( "click" );
            });

            $( "#ca-server-edit-btn" ).on( "click", function() {
              $( "li#caserversection" ).trigger( "click" );
            });

            $( "#hems-edit-btn" ).on( "click", function() {
              $( "li#hems" ).trigger( "click" );
            });

            $( "#backhaul-edit-btn" ).on( "click", function() {
              $( "li#backhaulstep" ).trigger( "click" );
            });

             $( "#fronthaul-edit-btn" ).on( "click", function() {
              $( "li#fronthaul" ).trigger( "click" );
            });

            $( "#redundany-edit-btn" ).on( "click", function() {
              $( "li#redundancy" ).trigger( "click" );
            });

            $( "#bclock-edit-btn" ).on( "click", function() {
              $( "li#bclock" ).trigger( "click" );
            });

            $( "#gobackstep1-btn" ).on( "click", function() {
              $( "li#questionnaire" ).trigger( "click" );
            });

            $("#summarypage").on("added-class", function() {
                var mgmtForm = $("#mgmtinterfaceconfigForm [type!='hidden']").serializeArray();
    	        var bclockForm = $("#boundaryClockForm [type!='hidden']").serializeArray();
                var fronthaulForm = $("#frontHaulConfigForm [type!='hidden']").serializeArray();
                var redundancyForm = $("#redundancyForm [type!='hidden']").serializeArray();
                redundancyForm = redundancyForm.concat($('#redundancyForm input[type=checkbox]:not(:checked)').map(
                                function() {
                                    return {"name": this.name, "value": this.value}
                                }).get()
                );

                var backhaulFormS1 = $("#backhaulFormS1 [type!='hidden']").serializeArray();
                var backhaulS1Gateway = $("#backhaulS1Gateway [type!='hidden']").serializeArray();
                var oamConfigForm = $("#oamConfigForm [type!='hidden']").serializeArray();
                var backhaulOAMGateway = $("#backhaulOAMGateway [type!='hidden']").serializeArray();
    	        var hemsForm = $("#hemsConfigForm [type!='hidden']").serializeArray() ;


                var caServerConfigForm = $("#caServerConfigForm [type!='hidden']").serializeArray();
                var snmpConfigForm = $("#snmpConfigForm [type!='hidden']").serializeArray();
                snmpConfigForm = snmpConfigForm.concat($('#snmpConfigForm input[type=checkbox]:not(:checked)').map(
                                function() {
                                    return {"name": this.name, "value": this.value}
                                }).get()
                );


                var mgmtConfigSummary = $("#mgmtConfigSummary");
                var bclockSummary = $("#bclockSummary");
                var fronthaulSummary = $("#fronthaulSummary");
                var redundancySummary = $("#redundancySummary");

                var s1Summary = $("#s1Summary");
                var s1GSummary = $("#s1GSummary");
                var oamSummary = $("#oamSummary");
                var oamGSummary = $("#oamGSummary");
                var hemsSummary = $('#hemsSummary');
                var caServerSummary =  $('#caServerSummary');
                var snmpSummary = $('#snmpSummary');
                var rootCertSummary = $('#rootCertSummary');
    	        mgmtConfigSummary.html('');
    	        bclockSummary.html('');
    	        fronthaulSummary.html('');
    	        redundancySummary.html('');
    	        s1Summary.html('');
    	        s1GSummary.html('');
    	        oamSummary.html('');
    	        oamGSummary.html('');
                hemsSummary.html('');
                caServerSummary.html('');
                snmpSummary.html('');
                rootCertSummary.html('');

                rootCertSummary.append($('#rootcertDiv').clone());
                renderSummary(mgmtForm,mgmtConfigSummary);
                renderSummary(bclockForm,bclockSummary);
                renderSummary(fronthaulForm,fronthaulSummary);
                renderSummary(redundancyForm,redundancySummary);

                renderSummary(backhaulFormS1,s1Summary);
                renderSummary(backhaulS1Gateway,s1GSummary);
                renderSummary(oamConfigForm,oamSummary);
                renderSummary(backhaulOAMGateway,oamGSummary);
                renderSummary(hemsForm,hemsSummary);
                renderSummary(caServerConfigForm,caServerSummary);
                renderSummary(snmpConfigForm,snmpSummary);
                });
            //$("#summarypage").addClass("active").trigger("added-class");

            function renderSummary(form_id,summary)
            {
                $.each(form_id, function(i, field)
                {
                    summary.append('<div class="divspace"><label>'+field.name+'</label>' + ":<label>" + field.value + "</label></div>");
                });
            }

            $("a").click(function(e){
                   //e.preventDefault();
                });

            if($('#id_SNMPTraps').val() == 'on')
            {
                $('#snmpConfigForm').show();
                $('#snmpConfigForm :input').prop('disabled',false);
            }
            else {
               $('#snmpConfigForm').hide();
               $('#snmpConfigForm :input').prop('disabled',true);
            }

            $('#id_SNMPTraps').on('change',function()
    	    {
    	    if($('#id_SNMPTraps').val() == 'on')
            {
                $('#snmpConfigForm').show();
                $('#snmpConfigForm :input').prop('disabled',false);
            }
            else {
               $('#snmpConfigForm').hide();
               $('#snmpConfigForm :input').prop('disabled',true);
            }

    	    });

            if($('#id_USM').is(':checked'))
            {
                $('#snmpConfigForm').find('div.usm_enable').show();
                $('#snmpConfigForm').find('div.usm_enable :input').prop('disabled',false);
            }
            else
            {
                $('#snmpConfigForm').find('div.usm_enable').hide();
                $('#snmpConfigForm').find('div.usm_enable :input').prop('disabled',true);
            }

    	    $('#id_USM').on('change',function()
    	    {
    	        if($(this).is(':checked'))
    	        {
    	            $('#snmpConfigForm').find('div.usm_enable :input').prop('disabled',false);
                    $('#snmpConfigForm').find('div.usm_enable').show();

    	        }
    	        else
    	        {
    	            $('#snmpConfigForm').find('div.usm_enable :input').prop('disabled',true);
    	            $('#snmpConfigForm').find('div.usm_enable').hide();

    	        }
    	    });

            var backhaulvalid;
            var mgmtStep;
            var backhaulStep;
            var bclock;
            var fronthaulStep;
            var rdncyStep;
            function checkNetworkInterfaceConfigValidity() {
                if(mgmtStep && bclock && fronthaulStep && rdncyStep)
                {
                   $('#nic_status').addClass('step_success');
                }
                else
                {
                   $('#nic_status').removeClass('step_success');
                   $('#nic_status').addClass('step_error');
                }
            }


             $('#mgmtinterfaceconfigForm').validate("ajax/validate_mgmtPortConfigForm/",
                {
                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#mgmtinterfaceconfigFormNav').removeClass('fa fa-times errorlist');
                        $('#mgmtinterfaceconfigFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        mgmtStep = true;
                        checkNetworkInterfaceConfigValidity()

                    },
                    fieldInvalidCallback: function(field) {
                        $('#mgmtinterfaceconfigFormNav').removeClass('fa fa-check success_color');
                        $('#mgmtinterfaceconfigFormNav').addClass('fa fa-times errorlist');
                        mgmtStep = false;
                        checkNetworkInterfaceConfigValidity()
                    }
                }
            );

            $('#nominalGpsForm').validate("ajax/validate_nominalgps/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#boundaryClockFormNav').removeClass('fa fa-times errorlist');
                        $('#boundaryClockFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();

                    },
                    fieldInvalidCallback: function(field) {
                        $('#boundaryClockFormNav').removeClass('fa fa-check success_color');
                        $('#boundaryClockFormNav').addClass('fa fa-times errorlist');
                    }
                }
            );

            $('#boundaryClockForm').validate("ajax/validate_boundaryclock/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#boundaryClockFormNav').removeClass('fa fa-times errorlist');
                        $('#boundaryClockFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        bclock = true;
                        checkNetworkInterfaceConfigValidity()

                    },
                    fieldInvalidCallback: function(field) {
                        $('#boundaryClockFormNav').removeClass('fa fa-check success_color');
                        $('#boundaryClockFormNav').addClass('fa fa-times errorlist');
                        bclock = false;
                        checkNetworkInterfaceConfigValidity()
                    }
                }
            );

            $('#backhaulFormS1').validate("ajax/validate_backHaulS1/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#backhaulFormNav').removeClass('fa fa-times errorlist');
                        $('#backhaulFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();

                    },
                    fieldInvalidCallback: function(field) {
                        $('#backhaulFormNav').removeClass('fa fa-check success_color');
                        $('#backhaulFormNav').addClass('fa fa-times errorlist');
                    }
                }
            );

            $('#backhaulS1Gateway').validate("ajax/validate_backHaulS1Gateway/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#backhaulFormNav').removeClass('fa fa-times errorlist');
                        $('#backhaulFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();

                    },
                    fieldInvalidCallback: function(field) {
                        $('#backhaulFormNav').removeClass('fa fa-check success_color');
                        $('#backhaulFormNav').addClass('fa fa-times errorlist');
                    }
                }
            );

            $('#oamConfigForm').validate("ajax/validate_backHaulOAM/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#backhaulFormNav').removeClass('fa fa-times errorlist');
                        $('#backhaulFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();

                    },
                    fieldInvalidCallback: function(field) {
                        $('#backhaulFormNav').removeClass('fa fa-check success_color');
                        $('#backhaulFormNav').addClass('fa fa-times errorlist');
                    }
                }
            );

            $('#backhaulOAMGateway').validate("ajax/validate_backHaulOAMGateway/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#backhaulFormNav').removeClass('fa fa-times errorlist');
                        $('#backhaulFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();

                    },
                    fieldInvalidCallback: function(field) {
                        $('#backhaulFormNav').removeClass('fa fa-check success_color');
                        $('#backhaulFormNav').addClass('fa fa-times errorlist');
                    }
                }
            );

            $('#frontHaulConfigForm').validate("ajax/validate_frontHaulform/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#frontHaulConfigFormNav').removeClass('fa fa-times errorlist');
                        $('#frontHaulConfigFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        fronthaulStep = true;
                        checkNetworkInterfaceConfigValidity()
                    },
                    fieldInvalidCallback: function(field) {
                        $('#frontHaulConfigFormNav').removeClass('fa fa-check success_color');
                        $('#frontHaulConfigFormNav').addClass('fa fa-times errorlist');
                        fronthaulStep=false;
                        checkNetworkInterfaceConfigValidity()
                    }
                }
            );

            $('#redundancyForm').validate("ajax/validate_redundancyForm/",
                {
                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#redundancyFormNav').removeClass('fa fa-times errorlist');
                        $('#redundancyFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        rdncyStep = true;
                        checkNetworkInterfaceConfigValidity()
                    },
                    fieldInvalidCallback: function(field) {
                        $('#redundancyFormNav').removeClass('fa fa-check success_color');
                        $('#redundancyFormNav').addClass('fa fa-times errorlist');
                        rdncyStep = false;
                        checkNetworkInterfaceConfigValidity()
                    }
                }
            );

            $('#snmpConfigForm').validate("ajax/validate_snmpForm/",
                {
                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $(form).find('div.alert').remove();
                        $('#snmp_step').addClass('step_success');
                    },
                    fieldInvalidCallback: function(field) {
                        $('#snmp_step').removeClass('step_success');
                        $('#snmp_step').addClass('step_error');
                    }
                }
            );

            var hemsStep;
            var caStep;
            $('#hemsConfigForm').validate("ajax/validate_hemsForm/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#hemsConfigFormNav').removeClass('fa fa-times errorlist');
                        $('#hemsConfigFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        hemsStep = true;
                        checkOperatorConfigValidity();
                    },
                    fieldInvalidCallback: function(field) {
                        $('#hemsConfigFormNav').removeClass('fa fa-check success_color');
                        $('#hemsConfigFormNav').addClass('fa fa-times errorlist');
                        hemsStep = false;
                        checkOperatorConfigValidity();
                    }
                }
            );

            function checkOperatorConfigValidity() {
                if(hemsStep && caStep)
                {
                   $('#operator_status').addClass('step_success');
                }
                else
                {
                   $('#operator_status').removeClass('step_success');
                   $('#operator_status').addClass('step_error');
                }
            }


            $('#caServerConfigForm').validate("ajax/validate_caServerForm/",
                {

                    fields: true,
                    event: 'change',
                    fieldSuccessCallback: function(field) {
                    },
                    formSuccessCallback: function(form) {
                        $('#caServerConfigFormNav').removeClass('fa fa-times errorlist');
                        $('#caServerConfigFormNav').addClass('fa fa-check success_color');
                        $(form).find('div.alert').remove();
                        caStep = true;
                        checkOperatorConfigValidity()
                    },
                    fieldInvalidCallback: function(field) {
                        $('#caServerConfigFormNav').removeClass('fa fa-check success_color');
                        $('#caServerConfigFormNav').addClass('fa fa-times errorlist');
                        caStep = false;
                        checkOperatorConfigValidity();
                    }
                }
            );


            $("#backhaulstep").click(function()
		     {
                if ($("#id_bc_mme_communication_1").is(":checked") && $("#id_bc_hems_communication_2").is(":checked") && $("#id_bc_ca_communication_2").is(":checked")) {
                    $("#s1configuration").show();
                    $("#s1Gateway").hide();
                    $("#oamgateway").hide();
                    $("#oamconfig").hide();
                }
                if($("#bhport").is(":checked")) {

                }

                if(($("#id_bc_mme_communication_0").is(":checked") && $("#id_bc_hems_communication_2").is(":checked")) || ($("#id_bc_mme_communication_0").is(":checked") && $("#id_bc_hems_communication_0").is(":checked")))
                {
                    $("#s1configuration").show();
                    $("#s1Gateway").show();
                    $("#oamgateway").hide();
                    $("#oamconfig").hide();
                }
                if(($("#id_bc_mme_communication_0").is(":checked") && $("#id_bc_hems_communication_1").is(":checked")))
                {
                    $("#s1configuration").show();
                    $("#s1Gateway").show();
                    $("#oamgateway").show();
                    $("#oamconfig").show();
                }

		    });



        }

        function toggleMode()
        {
            var mode_id = {'id_Mode_1':'mgmtinterfaceconfigForm','s1_mode_1':'backhaulFormS1','oam_mode_1':'oamConfigForm','bc_mode_1':'boundaryClockForm','rdncy_mode_1':'redundancyForm'}
            for(var key in mode_id)
            {
                if (mode_id.hasOwnProperty(key)) {
                var val = mode_id[key];
                if($('#'+key).is(':checked'))
               {
                $('#'+val).find('div.static :input').prop('disabled', true);
                $('#'+val).find('div.static').hide();

               }
               else
               {
                   $('#'+val).find('div.static :input').prop('disabled', false);
                  $('#'+val).find('div.static').show();

               }
              }
            }


            $("input[name='Mode']").change(function(){

               if($('#id_Mode_1').is(':checked'))
               {
                    $('#mgmtinterfaceconfigForm').find('div.static :input').prop('disabled', true);
                    $('#mgmtinterfaceconfigForm').find('div.static').hide();
               }
               else
               {
                   $('#mgmtinterfaceconfigForm').find('div.static :input').prop('disabled', false);
                  $('#mgmtinterfaceconfigForm').find('div.static').show();

               }

               if($('#s1_mode_1').is(':checked'))
               {
                    $('#backhaulFormS1').find('div.static :input').prop('disabled', true);
                    $('#backhaulFormS1').find('div.static').hide();
               }
               else
               {
                   $('#backhaulFormS1').find('div.static :input').prop('disabled', false);
                   $('#backhaulFormS1').find('div.static').show();

               }

               if($('#oam_mode_1').is(':checked'))
               {
                    $('#oamConfigForm').find('div.static :input').prop('disabled', true);
                    $('#oamConfigForm').find('div.static').hide();
               }
               else
               {
                   $('#oamConfigForm').find('div.static :input').prop('disabled', false);
                   $('#oamConfigForm').find('div.static').show();

               }


               if($('#bc_mode_1').is(':checked'))
               {
                    $('#boundaryClockForm').find('div.static :input').prop('disabled', true);
                    $('#boundaryClockForm').find('div.static').hide();

               }
               else
               {
                   $('#boundaryClockForm').find('div.static :input').prop('disabled', false);
                   $('#boundaryClockForm').find('div.static').show();

               }

               if($('#rdncy_mode_1').is(':checked'))
               {
                    $('#redundancyForm').find('div.static :input').prop('disabled', true);
                    $('#redundancyForm').find('div.static').hide();

               }
               else
               {
                   $('#redundancyForm').find('div.static :input').prop('disabled', false);
                   $('#redundancyForm').find('div.static').show();
               }



               });
        }


            var count;
            //var interval = null;

            function applyconfig_ajax() {
              $.ajax({
               type: "GET",
               //url: "/applyConfiguration/",
               data: "user=success",
               success: function(msg){
                    /*if(msg)
                    {
                        interval = setInterval(function() {
                              current_progress += 10;
                              $("#apply-progressbar")
                              .css("width", current_progress + "%")
                              .attr("aria-valuenow", current_progress)
                              .text(current_progress + "% Complete");
                              if (current_progress >= 100)
                                  clearInterval(interval);
                                  renderLast();
                          }, 1000);
                    }
                    else
                    {
                       *//* renderLast();
                        clearInterval(interval);*//*
                    }*/
               }
             });
            }


        $('#apply-config-btn').on('click',function()
        {
            $('#summarydiv').hide();
            $('#leftnavigation').find('li').addClass('disable_nav');
            $('#leftnavigation').find('li').off('click');
            $('#leftnavigation').find('li').click(function() { return false; }); // Adds another click event
            $('.btn-toolbar').remove();
            $('#apply-progress').removeClass('hide');
            //interval = setInterval("applyconfig_ajax()",5000);
            dummyprogress();
        }
        );

        function dummyprogress()
        {
            var current_progress = 0;
               var interval = setInterval(function() {
                              current_progress += Math.floor(Math.random() * 10);
                              $("#apply-progressbar")
                              .css("width", current_progress + "%")
                              .attr("aria-valuenow", current_progress)
                              .text(current_progress + "% Complete");
                              if (current_progress >= 100)
                              {
                                clearInterval(interval);
                                renderLast();
                              }
                          }, 500);
        }

        function renderLast()
        {
            $('#apply-progress').addClass('hide');
            $('#config-success').removeClass('hide');
        }

        $('#whitelistForm').submit(function(event){
        event.preventDefault()
        var formData = new FormData($(this)[0]);
        $.ajax({
                url: '/whitelist_upload/',
                type: 'POST',
                data: formData,
                async: true,
                beforeSend: function() {
                    $("#loading-image_whitelist").show();
                    $("#whitelist_upload_status").hide();
                },
                success: function (data) {

                console.log(data)
                $("#loading-image_whitelist").hide();
                $("#whitelist_upload_status").show();
                var tableData = [];
                if (data.status == "success"){
                var whitelist_string = data.result;
                var split_comma = whitelist_string.split(",");
                for (i = 0; i < split_comma.length; i++) {
                    var split_semicolon = split_comma[i].split(";");
                    var collocated_RP = [];
                        for (j = 0; j < split_semicolon.length; j++) {
                            collocated_RP.push(split_semicolon[j]);
                    }
                    if(collocated_RP.length == 1)
                        collocated_RP.push("");
                    tableData.push(collocated_RP);
                    }
                    data.result="Whitelist Processed successfully";
                    console.log(tableData)
                    /*if ($('#example').DataTable().data().any() ) {
                        console.log("has data")
                        $('#example').DataTable().fnClearTable();
                    }*/
                $('#whitelist_table').DataTable( {
                    "bPaginate": true,
                    "bLengthChange": true,
                    "bFilter": true,
                    "bSort": true,
                    "bAutoWidth": true,
                    "pageLength": 50,
                    data: tableData,
                    columns: [
                        {
                            title: "Sector1"
                        },
                        {
                            title: "Sector2"
                        }
                    ],
                } );
                /*$('#whitelist_table').Tabledit({
                editButton: false,
                hideIdentifier: true,
                columns: {
                }
            });*/
            $('#whitelist_table td').quickEdit(
                {
                    blur: false,
                    checkold: true,
                    space: false,
                    //maxLength: 50,
                    showbtn: false,
                    submit: function (dom, newValue) {
                        dom.text(newValue);
                    }
                });

                }else{
                    $('#whitelist_table').dataTable().fnClearTable();
                }
                $("#whitelist_upload_status_success").html(data.result)
                },
                error: function (data) {
                $("#whitelist_upload_status_error").html(data.result)
				$("#whitelist_upload_status_error").show();
                },
                cache: false,
                contentType: false,
                processData: false
        });
        return false;
});


        $(document).keydown(function(e) {
            switch(e.which) {
                case 37:
                $( "button#prev" ).trigger( "click" );
                break;

                case 39:
                $( "button#next" ).trigger( "click" );
                break;

                default: return; // exit this handler for other keys
            }
            e.preventDefault(); // prevent the default action (scroll / move caret)
            });



           /* function initWizardNav()
            {
                var BootstrapWizard = function(element, options) {
                    this.$element   = $(element);
                    this.options    = $.extend({}, $.fn.bootstrapWizard.DEFAULTS, options);
                    this.$prev      = $([]);
                    this.$current   = $([]);
                    this.$next      = $([]);

                    this.$nav = $('<nav class="navbar-default" role="navigation">'
                                        +'<div class="wizard-nav-header visible-xs-block">'
                                            +'<button type="button" class="navbar-toggle pull-left margin left" data-toggle="collapse" data-target=".wizard-nav">'
                                                +'<span class="sr-only">Toggle navigation</span>'
                                                +'<span class="icon-bar"></span>'
                                                +'<span class="icon-bar"></span>'
                                                +'<span class="icon-bar"></span>'
                                            +'</button>'
                                            +'<h3 class="wizard-nav-title"></h3>'
                                        +'</div>'
                                        +'<div class="wizard-nav collapse in">'
                                        +'</div>'
                                        +'<div class="progress hidden-xs">'
                                            +'<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%">'
                                            +'</div>'
                                        +'</div>'
                                    +'</nav>');

                    this.$body = $('<div class="wizard-body">'
                                        +'<div class="wizard-content">'
                                        +'</div>'
                                        +'<div class="wizard-footer">'
                                            +'<div class="btn-toolbar">'
                                                +'<div class="btn-group">'
                                                    +'<button class="btn btn-danger wizard-cancel" type="button">'+this.options.buttonText.cancel+'</button>'
                                                +'</div>'
                                                +'<button class="btn btn-success wizard-submit pull-right" type="button">'+this.options.buttonText.submit+'</button>'
                                                +'<button id="next" class="step-fll-prev step-fll next wizard-next pull-right" type="button">'+this.options.buttonText.next+'<i class="fa fa-angle-right" aria-hidden="true"></i></button>'
                                                +'<button id="prev" class="step-fll-prev step-prev prev wizard-back pull-right" type="button">'+this.options.buttonText.back+'<i class="fa fa-angle-left" aria-hidden="true"></i></button>'
                                                 +'<button class="btn btn-default wizard-clear pull-left clear-config-btn" type="button">'+this.options.buttonText.clear+'</button>'
                                            +'</div>'
                                        +'</div>'
                                    +'</div>');

                    this._init();
                };

                BootstrapWizard.prototype = {
                    constructor: BootstrapWizard,

                    _init: function() {
                        var wizard          = this;
                        var $navList        = this.$element.children('ul.nav-wizard'); //.addClass("navbar-nav")
                        var progressHeight  = 0;

                        this.$element.append(this.$nav, this.$body).css({
                            "width":(this.options.width?this.options.width+"px":"auto"),
                            "height":this.options.height+"px"
                        });
                        this.$nav.children(".wizard-nav").prepend($navList);

                        var $wizardFooter   = this.$body.find(".wizard-footer");
                        var $cancelButton   = $wizardFooter.find(".wizard-cancel");
                        this.$clearButton     = $wizardFooter.find(".wizard-clear").on("click", this.clear);
                        this.$backButton     = $wizardFooter.find(".wizard-back").on("click", this.back);
                        this.$nextButton     = $wizardFooter.find(".wizard-next").on("click", this.next);
                        this.$submitButton   = $wizardFooter.find(".wizard-submit").on("click", this.submit);
                        this.$nav.find(".navbar-toggle").on("click", function(event){
                           $(this).parents("nav").find(".wizard-nav").collapse("toggle");
                        });

                        if ( this.options.cancelButton )
                            $cancelButton.show();

                        if ( !this.options.footerButtons )
                            $wizardFooter.find(".btn-toolbar").hide();

                        if ( this.options.progressBar )
                            progressHeight = this.$nav.find(".progress").outerHeight();
                        else
                            this.$nav.find(".progress").hide();

                        var contentHeight = this.options.height - $wizardFooter.outerHeight() - 30;
                        // var navListHeight = this.options.height - progressHeight - 30;

                        this.$body.height((this.options.height-30)+"px");
                        // $navList.height(navListHeight+"px");
                        this.$body.find('.wizard-content').css({
                            //"height":contentHeight+"px",
                            //"overflow-y":""
                        }).append(
                            this.$element.children('.wizard-pane').css("visibility","visible").hide()
                        );

                        *//* metismenu - https://github.com/onokumus/metisMenu *//*
                        $navList.find("li.active").has("ul").children("ul").addClass("collapse in");
                        $navList.find("li").not(".active").has("ul").children("ul").addClass("collapse");
                        $navList.find("li").has("ul").children("a").append('<span class="caret"></span>');

                        $navList.on("click.bw", "li", function(event){
                            event.preventDefault();
                            event.stopPropagation();
                            $li = $(this);
                            if ( !$li.is(".visited") || $li.is(".disabled") )
                                return;

                            $li.parents(".wizard").data("bootstrapWizard").show($li);
                        });

                        $(window).on("resize.bw", function(){
                            $(".wizard").data("bootstrapWizard")._resize();
                        });

                        this.$element.css("visibility", "visible").show();
                        this.show($navList.find("li:first"));
                    },

                    back: function(){
                        var wizard = $(this).parents(".wizard").data("bootstrapWizard");
                        wizard.show(wizard.$prev);
                    },

                    next: function(){
                        var wizard = $(this).parents(".wizard").data("bootstrapWizard");
                        wizard.show(wizard.$next);
                    },

                    show: function($li){

                        var relatedTarget = this.$current;
                        var relatedPane = this.$body.find( this.$current.find("a").attr("href") );

                        var e = $.Event('show.bw', {
                            'relatedTarget': relatedTarget,
                            'relatedPane': relatedPane
                        });
                        $li.trigger(e);
                        if (e.isDefaultPrevented()) return;

                        this.$current = $li.addClass("visited active").trigger("added-class");
                        href = this.$current.find("a").attr("href");


                        this.$current.siblings().removeClass("active").children("ul.in").collapse("hide");
                        if ( ($parentNav = this.$current.parent("ul.collapse")).length ) {
                            $parentNav.collapse("show").parent("li").addClass("active").siblings().removeClass("active").children("ul.in").collapse("hide");
                        }
                        this.$prev = this.$current.prevAll(":not(.disabled):first");
                        if ( !this.$prev.length ) {
                            this.$prev = this.$current.parents("li.active");
                            if ( this.$prev.find("a").attr("href") == '' ) {
                                this.$prev = this.$prev.prevAll(":not(.disabled):first");
                            }
                        } else if ( ($childNav = this.$prev.children("ul")).length ) {
                            $childNav.find("li.active").removeClass("active");
                            this.$prev = $childNav.children("li:not(.disabled):last");
                        }

                        if ( ($childNav = this.$current.children("ul")).length ) {
                            $childNav.collapse("show").find("li.active").removeClass("active");
                            this.$next = $childNav.children("li:not(.disabled):first");
                            if ( href == '' ) {
                                this.$current = this.$next.addClass("visited active").trigger("added-class");
                                this.$next = this.$current.nextAll(":not(.disabled):first");
                                href = this.$current.find("a").attr("href");
                            }
                        } else {
                            this.$next = this.$current.nextAll(":not(.disabled):first");
                        }
                        if ( !this.$next.length ) {
                            this.$next = this.$current.parents("li.active").nextAll(":not(.disabled):first");
                        }

                        if ( this.$prev.length ) {
                            this.$backButton.show();
                        } else {
                            this.$backButton.hide();
                        }

                        if ( this.$next.length ) {
                            this.$nextButton.show();
                            this.$submitButton.hide();
                        } else {
                            this.$nextButton.hide();
                            this.$submitButton.show();
                        }

                        this.$body.find(".wizard-pane:visible").hide();
                        this.$body.find( href ).show();
                        if ( this.$nav.find(".wizard-nav-header").is(":visible") ) {
                            var navTitle = this.$current.children("a").text();
                            if ( ($parentNav = this.$current.parent("ul.collapse")).length ) {
                                navTitle = $parentNav.parent("li").children("a").text() + ' > ' + navTitle;
                            }
                            this.$nav.find("h3.wizard-nav-title").text(navTitle);
                            this.$nav.find(".wizard-nav").collapse("hide");
                        }

                    },

                    _resize: function() {
                        console.log(this);
                        if ( this.$nav.find(".wizard-nav-header").is(":visible") ) {
                            this.$element.css({
                                "width":"auto",
                                "height": "560px"
                            });
                            this.$body.height((560 - this.$nav.find(".wizard-nav-header").outerHeight())+"px");
                            this.$body.find('.wizard-content').height( (this.$body.innerHeight() - this.$body.find(".wizard-footer").outerHeight() - 30)+"px" );
                            this.$nav.find(".wizard-nav").collapse("hide");
                        } else {
                            this.$nav.find(".wizard-nav").collapse("show");
                        }
                    },

                    submit: function(){
                        var wizard = $(this).parents(".wizard").data("bootstrapWizard");

                        var relatedTarget = wizard.$current;
                        var relatedPane = wizard.$body.find( wizard.$current.find("a").attr("href") );

                        var e = $.Event('show.bw', {
                            'relatedTarget': relatedTarget,
                            'relatedPane': relatedPane
                        });
                        wizard.$current.trigger(e);
                        if (e.isDefaultPrevented()) return;

                        e = $.Event('submit.bw', {});
                        $(this).trigger(e);
                        if (e.isDefaultPrevented()) return;

                    },

                    markAllVisited: function(){
                        this.$nav.find("li").addClass("visited");
                    },

                    serialize: function(){
                        return this.$body.find(".wizard-pane form").serialize();
                    },

                    progress: function (percent) {
                        this.$nav.find(".progress-bar")
                            .attr('aria-valuenow', percent)
                            .css('width', value + '%')
                            children("span").text(percent + '%');
                    }


                };

                $.fn.bootstrapWizard = function(option) {
                    return this.each(function () {
                        var $this   = $(this);
                        var data    = $this.data('bootstrapWizard');
                        var options = typeof option == 'object' && option;

                        if (!data) {
                            data = new BootstrapWizard(this, options);
                            $this.data('bootstrapWizard', data);
                        }
                        if (typeof option == 'string') {
                            data[option]();
                        }
                    })
                };

                $.fn.bootstrapWizard.DEFAULTS = {
                    width: null,
                    height: 900,
                    cancelButton: false,
                    footerButtons: true,
                    progressBar: true,
                    buttonText: {
                        cancel: "Cancel",
                        next: "",
                        back: "",
                        submit: "Submit",
                        clear:"Clear Configuration",
                    }
                };

                $.fn.bootstrapWizard.Constructor = BootstrapWizard;
                $(".wizard").bootstrapWizard({
                    height: '600',
                });
            }*/
