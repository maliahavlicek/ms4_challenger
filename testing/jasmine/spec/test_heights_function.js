
// tests for matching heights, used by products, home, and all entry pages, this
describe('Test alignItems function', function () {
    beforeEach(() => {
        setFixtures(`
            <div class="container-fluid rocket">
        <div class="main-item">
            <div class="row">
                <div class="col-md-4">
                    <h4 class="tutorial-head">Registering</h4>
                    <div class="text">a lot of word@! a lot of word@!a lot of word@!a lot of word@!a lot of word@!a lot of word@!a lot of word@!a lot of word@!a lot of word@!a lot of word@!</div>
                </div>
                <div class="col-md-4">
                    <h4 class="tutorial-head">Creating A Challenge is a medium sized bit of a title</h4>
                    <div class="text">not so many</div>
                </div>
                <div class="col-md-4">
                    <h4 class="tutorial-head">Submitting An Entry Submitting An Entry Submitting An EntrySubmitting An EntrySubmitting An EntrySubmitting An EntrySubmitting An EntrySubmitting An Entry</h4>
                    <div class="text">A bit more wordy than your average test block of stuff but it'll do.</div>
                </div>
            </div>
        </div>
    </div>
        `);
    });

    it('Test alignItems: match heights single selector', function () {
        //set up list of selectors you want to even up
        var selectors = ['.tutorial-head'];
        alignItems(selectors, false);
        var height = $('.tutorial-head')[0].getAttribute('style');
        $('.tutorial-head').each(function (i) {
            expect($('.tutorial-head')[i].getAttribute('style')).toEqual(height);
        });

        // make sure extras were not evened up
        var height = $('.text')[0].getAttribute('style');
        $('.text').each(function (i) {
            if (i != 1) {
                expect($('.text')[i].getAttribute('style')).toEqual(height);
            }
        });
    });

    it('Test alignItems: multiple selectors', function () {
        //set up list of selectors you want to even up
        var selectors = ['.tutorial-head', '.text'];
        alignItems(selectors, false);

        var height = $('.tutorial-head')[0].getAttribute('style');
        $('.tutorial-head').each(function (i) {
            expect($('.tutorial-head')[i].getAttribute('style')).toEqual(height);
        });

        var height = $('.text')[0].getAttribute('style');
        $('.text').each(function (i) {
            expect($('.text')[i].getAttribute('style')).toEqual(height);
        });
    });

    it('Test alignItems: does not fail if selector not found', function () {
        //set up list of selectors you want to even up
        var selectors = ['.whatever', '.texting'];
        alignItems(selectors, false);
        expect(true).toBe(true)
    });
});