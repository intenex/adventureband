// put all events in here - but not anything else? Because everything else breaks if you put it in here it seems
// and by event, I think things like the .one or .click - things that jQuery is actively checking for, things that you don't *call*, but will happen automatically if something is triggered in the DOM
$(document).ready(function() {

// Setting Attribute Point Distribution Values - NOTE: MUST BE GLOBAL VARIABLES TO BE ACCESSED OUTSIDE OF $(document).ready's anonymous function! To create a global variable merely omit the 'var' before defining the variable. All these values must 1. be defined in $(document).ready since this .js file is loaded before the values for the form/character are, and thus if these values were set before the DOM was loaded they would all be set to 'undefined' (learned from experience) and 2. they must be global variables to be accessed outside of $(document).ready's anonymous function, namely by the 'changeAttrib()' function
// http://stackoverflow.com/questions/3352020/jquery-the-best-way-to-set-a-global-variable
ini_str = $("input#id_strength").val();
ini_int = $("input#id_intelligence").val();
ini_wis = $("input#id_wisdom").val();
ini_dex = $("input#id_dexterity").val();
ini_con = $("input#id_constitution").val();
ini_cha = $("input#id_charisma").val();
hp = $("input#id_max_hp").val();
attrib_points = 30;
// {# need to keep a copy of initial values so the user can't decrease beyond these values #}
// {# these variables (strength/intelligence/etc) are the ones that will be changed by jQuery #}
strength = ini_str, intelligence = ini_int, wisdom = ini_wis, dexterity = ini_dex, constitution = ini_con, charisma = ini_cha;
// {# There must be a better way of doing this, but I haven't thought of it yet :D #}
$("p#attrib_points").html('Attribute Points Remaining: ' + attrib_points);
$("span#up_HP, span#down_HP").hide()

});// close $(document).ready()

// Attribute Point Distribution code (with arrows)
function changeAttrib(direction,attrib){
    if (direction == 'up') {
        if (attrib_points > 0) {
            if (attrib == 'Strength' && strength < 20) {
                strength++;
                attrib_points--;
                $("input#id_strength").val(strength);}
            else {
                if (attrib == 'Intelligence' && intelligence < 20) {
                    intelligence++;
                    attrib_points--;
                    $("input#id_intelligence").val(intelligence);}
                else {
                    if (attrib == 'Wisdom' && wisdom < 20) {
                        wisdom++;
                        attrib_points--;
                        $("input#id_wisdom").val(wisdom);}
                    else {
                        if (attrib == 'Dexterity' && dexterity < 20) {
                            dexterity++;
                            attrib_points--;
                            $("input#id_dexterity").val(dexterity);}
                        else {
                            if (attrib == 'Constitution' && constitution < 20) {
                                constitution++;
                                attrib_points--;
                                $("input#id_constitution").val(constitution);}
                            else {
                                if (attrib == 'Charisma' && charisma < 20) {
                                    charisma++;
                                    attrib_points--;
                                    $("input#id_charisma").val(charisma);}
                                else {
                                    alert('You cannot raise ' + attrib + ' anymore.');
            }}}}}} // {# closing all the else tags lol #}
        }
        else {
            alert('You have no more attribute points.');
        }
    }
    else {
        if (direction == 'down') {
            if (attrib == 'Strength' && strength > ini_str) {
                strength--;
                attrib_points++;
                $("input#id_strength").val(strength);}
            else {
                if (attrib == 'Intelligence' && intelligence > ini_int) {
                    intelligence--;
                    attrib_points++;
                    $("input#id_intelligence").val(intelligence);}
                else {
                    if (attrib == 'Wisdom' && wisdom > ini_wis) {
                        wisdom--;
                        attrib_points++;
                        $("input#id_wisdom").val(wisdom);}
                    else {
                        if (attrib == 'Dexterity' && dexterity > ini_wis) {
                            dexterity--;
                            attrib_points++;
                            $("input#id_dexterity").val(dexterity);}
                        else {
                            if (attrib == 'Constitution' && constitution > ini_con) {
                                constitution--;
                                attrib_points++;
                                $("input#id_constitution").val(constitution);}
                            else {
                                if (attrib == 'Charisma' && charisma > ini_cha) {
                                    charisma--;
                                    attrib_points++;
                                    $("input#id_charisma").val(charisma);}
                                else {
                                    alert('You cannot lower ' + attrib + ' anymore.');
            }}}}}}
        }
    }
    $("p#attrib_points").html('Attribute Points Remaining: ' + attrib_points);
    hp = constitution / 2;
    $("input#id_max_hp").val(parseInt(hp));
}
// End Attribute Point Distribution code









