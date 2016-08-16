var google = google || {};
google.appengine = google.appengine || {};
google.appengine.hopster = google.appengine.hopster || {};
google.appengine.hopster.diary = google.appengine.hopster.diary || {};
google.appengine.hopster.diary.api_ready = false;
google.appengine.hopster.diary.apiRoot = '';
google.appengine.hopster.diary.init = function(apiRoot) {
    var apisToLoad;
    google.appengine.hopster.diary.apiRoot = apiRoot;
    var callback = function() {
        if (--apisToLoad == 0) {
            google.appengine.hopster.diary.api_ready = true;
        }
    };

    apisToLoad = 2;
    gapi.client.load('diary', 'v1', callback, apiRoot);
    gapi.client.load('user', 'v1', callback, apiRoot);
};

google.appengine.hopster.diary.list = function (token, callback) {
    path = document.location.origin + '/_ah/api';

    request = gapi.client.request({
          'path': path + '/diary/v1/list',
          'headers': {'Authorization': 'Bearer ' + token}
        }

    );
    request.execute(callback);
};