$(document).ready(function(){

    var template = $(".audio-lang-select li.audio-language").first().clone();
    $(".audio-lang-select li.audio-language").remove();
    
    $($("input[name='audioLangs']").val().split("|")).each(function(){
        var parts = this.split(":");

        language = template.clone();
        language.find("select").val(parts[0]);
        if(parseInt(parts[1]) == 1)
            language.find("input:checkbox").attr('checked', true);
        else
            language.find("input:checkbox").attr('checked', false);

        $(".audio-lang-select").append(language);
    });

    function updateAudioSelectContext(){
        var languages = $(".audio-lang-select li.audio-language");
        if (languages.length > 1) {
            languages.find("input, .icon-remove").css("visibility", "visible");
        } else {
            languages.find("input, .icon-remove").css("visibility", "hidden").attr("value", "1");
        }
    }
    updateAudioSelectContext();


    function updateAudioLanguages(){
        var languages = $(".audio-lang-select li.audio-language");
        audioLangs = [];
        languages.each(function(i){
            var language = $(this);
            var satisfied = language.find("input:checkbox:checked").length;
            audioLangs.push(language.find("select").val() + ":" + satisfied);
        });
        $("input[name='audioLangs']").val(audioLangs.join("|"));
    }
    updateAudioLanguages();

    var counter = 0;
    $(".add-language").unbind("click").click(function(){
        counter++;
        var template = $(".audio-lang-select li.audio-language").first().clone();
        template.html(template.html().replace(/\[0\]/g, "[" + counter + "]"));
        $(".audio-lang-select li.audio-language").last().after(template);
        updateAudioSelectContext();
        updateAudioLanguages();
        return false;
    });

    $(".audio-lang-select").find("input, select").live("change", function(){
        updateAudioLanguages();
        updateAudioSelectContext();
    })

    $(".audio-lang-select").find(".icon-remove").live("click", function(){
        $(this).parent("li").remove();
        updateAudioLanguages();
        updateAudioSelectContext();
    })

    $(".audio-lang-select").sortable({
        placeholder: 'ui-state-highlight',
        update: function (event, ui) {
            updateAudioLanguages();
        }
    });
});