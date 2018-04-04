function _x(STR_XPATH) {
    var xresult = document.evaluate(STR_XPATH, document, null, XPathResult.ANY_TYPE, null);
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }

    return xnodes;
}

var xpaths = {
    'cover': {
        'single': '//div[@class="article-cover"]//label[1]//input',
        'triple': '//div[@class="article-cover"]//label[2]//input',
        'auto': '//div[@class="article-cover"]//label[3]//input',
    },
    'ad': {
        'toutiao': '//div[@class="form-wrap"]/div[2]//label[1]//input',
        'self': '//div[@class="form-wrap"]/div[2]//label[2]//input',
        'none': '//div[@class="form-wrap"]/div[2]//label[3]//input',
    },
    'act': {
        },
    'action': {
        'publish': '//div[contains(@class, "figure-footer")]/div[@class="edit-input"]/div[1]'
    }
};

var targets = [
    ['cover', 'auto'],
    ['ad', 'toutiao'],
    ['action', 'publish']
];

for(var i=0; i<targets.length; i++) {
        var nodes = _x((xpaths[target[0]][target[1]]));
        console.log(nodes);
        nodes[0].click()
    }
