// tests member entry in challenges.js
describe('Test Member Entry via DOM', function () {
    var spyEvent;
    beforeEach(() => {
        //set handler for clicking Add Member Button
        spyEvent = spyOnEvent('#add_member', 'click');
    });
    it('Member Entry Test: error if entering same email', function () {
        //set email
        var email = document.getElementById('email').value = 'test1@test.com';
        $('#add_member').trigger("click");
        expect($('#error_email').hasClass('invalid-feedback')).toBe(false);

        //try to add same email again
        var email = document.getElementById('email').value = 'test1@test.com';
        $('#add_member').trigger("click");
        expect($('#error_email').hasClass('invalid-feedback')).toBe(true);

    });
    it('Member Entry Test: error if email is invalid', function () {
        // try to add invalid email
        var email = document.getElementById('email').value = 'test1@test';
        $('#add_member').trigger("click");
        expect($('#error_email').hasClass('invalid-feedback')).toBe(true);

    });
    it('Member Entry Test: error if member limit hit', function () {
        for (i = 0; i < 5; i++) {
            var tmp = 'test' + i.toString() + '1@test.com';
            var email = document.getElementById('email').value = tmp;
            $('#add_member').trigger("click");
            if (i < 4) {
                var val = JSON.parse($('#id_members').val());
                expect(JSON.stringify(val).indexOf(tmp) > -1).toBe(true);
            }
        }
        expect($('#member_list_errors').hasClass('is-invalid')).toBe(true);
        expect($('#error_member_list').hasClass('invalid-feedback')).toBe(true);

    });
    it('Member Entry Test: Remove Member', function () {
        //set email
        var tmp = 'test1@test.com';
        var email = document.getElementById('email').value = tmp;
        $('#add_member').trigger("click");

        var val = JSON.parse($('#id_members').val());
        expect(JSON.stringify(val).indexOf(tmp) > -1).toBe(true);

        $('a.member-remove').trigger("click");

        var val = JSON.parse($('#id_members').val());
        expect(JSON.stringify(val).indexOf(tmp) > -1).toBe(false);

    });
});
