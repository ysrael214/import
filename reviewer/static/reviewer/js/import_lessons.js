	
	var importLessons =  {

		 // Output Question // Randomize
         // Keyboard Detect // Press Enter Event
         // Check Answer // Check & Submit Answer 
         // Make Progress // Depends on Total
         // Reset // Reset Input Fields

		module_name: "importLessons",
		builder: {

			editor: undefined,
			script: {
				data : undefined,
				questions: undefined,
				qdata: undefined,
				load: function(){

					$(".import-code-console").empty();
					$(".import-code-iden-answer").fadeOut(300);

					let code = importApp.builder.editor.session.getValue();
					let errors = importApp.builder.editor.session.getAnnotations();
					let hasError = false;
					let retval = false;

					errors.forEach(function(item){
						if (item.type == "error"){
							console.log(`ERROR: ${item.text} (${item.row + 1}, ${item.column + 1})`);
							hasError = true;
						}
					});

					if (/<\/\s*script\s*>/ig.test(code)){
						alert("Closing script tags are not allowed.");
					}
					else if (/window\.location/ig.test(code)){
						alert("window.location is not allowed.");
					}
					else if (/importApp/g.test(code)){
						alert("Using importApp with the builder is not allowed.");
					}
					else if (!hasError){
						if (importApp.builder.script.data)
							$("#import-script").remove()

						importApp.builder.script.data = document.createElement("script");
						importApp.builder.script.data.innerHTML = code;
						document.body.appendChild(importApp.builder.script.data);
						importApp.builder.script.data.setAttribute("id", "import-script");
						$("#import-script").appendTo(".scripts");

						importApp.builder.script.questions = question();

						if (importApp.builder.script.questions != undefined && Array.isArray(importApp.builder.script.questions) ){
							importApp.builder.script.qdata = {
								remq: importApp.builder.script.questions,
								currentq: undefined
							}

							try{
								importApp.builder.script.qdata.currentq = Math.floor(Math.random() * importApp.builder.script.qdata.remq.length); 
								let currentq = importApp.builder.script.qdata.currentq;
								let currentq_data = importApp.builder.script.qdata.remq[currentq];

								if (!$(".import-math-subquestion").length)
									$(".import-question").html(currentq_data.question);

								//Multiple Choice
								if ($(".import-choices").length){
									$(".import-choices").empty();
									for (var choc = 0; choc < currentq_data.choices.length; choc++){
										$(".import-choices").append(`<div class="d-flex layer-container p-2 mb-2 import-choice">
											<div class="py-2 px-3 my-auto">
												${String.fromCharCode(65+choc)}
											</div>
											<div class="mx-2 my-auto import-choice-data">
												${currentq_data.choices[choc]}
											</div>
										</div>`);
										if (choc == 4)
											break;
									}
								}

								//Identification
								if ($(".import-subquestion").length && currentq_data.subquestion != undefined)
									$(".import-subquestion").html(currentq_data.subquestion);

								$(".import-code-iden-input").val("");
								$(".import-code-iden-submit").prop("disabled", true)
								$(".import-code-iden").fadeIn(50);

								//Math
								if (importApp.questions.math.loaded && $(".import-math-subquestion").length && currentq_data.subquestion != undefined){
									$(".import-question").html(currentq_data.question);
									$(".import-math-input").removeClass("d-none");
									$(".import-math-submit").removeClass("d-none");
									$(".import-math-submit").addClass("d-inline-flex");
									importApp.questions.math.input.setEditorState({"content": ""});
									$(".import-math-submit").prop("disabled", true);
									importApp.questions.math.graph.reset();

									if (currentq_data.graph == true){
										$(".import-math-graph").removeClass("h-0");
										importApp.questions.math.graph.evalCommand(currentq_data.subquestion);
										//importApp.questions.math.graph.setColor("f", 255, 145, 114);
									}
									else{
										$(".import-math-graph").addClass("h-0");
									}

									importApp.questions.math.given.setEditorState({"content": currentq_data.subquestion});
									let latexInput = importApp.questions.math.given.getEditorState().latex.replace(/\\nbsp/g, "\\space");
									$(".import-math-subquestion-latex").html(`$$\\sf ${currentq_data.latex == undefined? latexInput : currentq_data.latex.replace(/%importggb\.latex%/g, latexInput)} $$`);
									renderMathInElement(document.getElementById("import-ggb-q-latex"));
								}

								retval = true;
							}
							catch(err){
							}
						}
						else{
							alert("Question Set must be an array.");
						}
					}
					return retval;
				}
			},
			init: function(div_id){
				importApp.builder.editor =	ace.edit(div_id);
				importApp.builder.editor.session.setMode("ace/mode/javascript");
	    		importApp.builder.editor.session.setTabSize(2);
	    		importApp.builder.editor.setShowPrintMargin(false);
			}
		},

		questions:{

			create: function(that, url=window.location.href){

				if (importApp.requests.ajax)
					importApp.requests.ajax.abort();
				  
				var form = document.getElementById(that);
				var formData = new FormData(form);
				$(".import-question-create").prop("disabled", true);

				importApp.requests.ajax =  $.ajax({
					type: 'post',
					url: url,
					data: formData,
					cache: false,
					contentType: false,
					processData: false,
					complete: function(){ $(".import-question-create").removeAttr("disabled"); },
					success: function (response, status, xhr){
						if (response.error)
							alert(response.error)
						else{
							$("#importModal").modal('hide');
							if($(".lesson-question").length > 0){
								$(".questions").append(response.question);
								$(`.import-codelang .codelang-select option[value=${response.langID}]:not([selected])`).remove()
							}
							else{
								$(".questions").html(response.question);
							}
						}
				    }
				});
			},
			input:{
				allow: function(that){ ($(that).val().trim() == 0)? $(".import-code-iden-submit").prop("disabled", true): $(".import-code-iden-submit").removeAttr("disabled")},
				check: function(){

					let currentq = importApp.builder.script.qdata.currentq;
					let currentq_data = importApp.builder.script.qdata.remq[currentq]

					//Modify to work with actual lesson page
					if ($(".import-code-iden-input").length && $(".import-code-iden-input").val().trim().length > 0){
						let userInput = $(".import-code-iden-input").val().trim();
						let result = (typeof currentq_data.answer == 'function')? currentq_data.answer(userInput, currentq_data.subquestion, currentq_data.question):currentq_data.answer;

						$(".import-code-iden-answer .import-code-iden-rectans").html(result);
						$(".import-code-iden-answer").fadeIn(300);
						userInput == String(result)? importApp.questions.output.correct(): importApp.questions.output.wrong();
					}
					// Math
					else if ($(".import-math-input").length){
						let mathInputVal = importApp.questions.math.input.getEditorState().content;
						importApp.questions.math.input.setEditorState({content: mathInputVal});
						let result = (typeof currentq_data.answer == 'function')? currentq_data.answer(mathInputVal, currentq_data.subquestion, currentq_data.question):currentq_data.answer;

						let temp = importApp.questions.math.given.getEditorState().content;
						importApp.questions.math.given.setEditorState({'content': result});
						let resulttex = importApp.questions.math.given.getEditorState().latex.replace(/\\nbsp/g, "");
						importApp.questions.math.given.setEditorState({'content': temp});

						$(".import-code-iden-answer .import-code-iden-rectans").html(`\\(\\sf ${resulttex}\\)`);
						renderMathInElement(document.body);
						$(".import-code-iden-answer").fadeIn(300);
						mathInputVal == String(result)? importApp.questions.output.correct(): importApp.questions.output.wrong();
					}
				}
			},
			math: {
				given: undefined,
				input: undefined,
				graph: undefined,
				loaded: false
			},
			output: {
				correct: function(){
					$(".import-code-iden-answer .import-code-iden-answer-container").removeClass("import-quiz-wrong");
					$(".import-code-iden-answer .import-code-iden-answer-container").addClass("import-quiz-correct");
					$(".import-code-iden-answer .import-code-iden-answer-container .material-icons").html("done");
					$(".import-code-iden-answer .import-code-iden-stat").html("correct");
					document.getElementById("import-sound-correct").currentTime = 0;
					document.getElementById("import-sound-correct").play();
				},
				wrong: function(){
					$(".import-code-iden-answer .import-code-iden-answer-container").removeClass("import-quiz-correct");
					$(".import-code-iden-answer .import-code-iden-answer-container").addClass("import-quiz-wrong");
					$(".import-code-iden-answer .import-code-iden-answer-container .material-icons").html("close");
					$(".import-code-iden-answer .import-code-iden-stat").html("wrong");
					document.getElementById("import-sound-wrong").currentTime = 0;
					document.getElementById("import-sound-wrong").play();
				}
			}
		},
		init: function(){

		}
	}
	
	importApp.load(importLessons);
	delete importLessons;