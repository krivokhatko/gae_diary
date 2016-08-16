var RecordBox = React.createClass({
  loadNotesFromServer: function() {
      if(google.appengine.hopster.diary.api_ready){
          var token = sessionStorage.getItem('accessToken') || null;
          if (token) {
              google.appengine.hopster.diary.list(
                  token,
                  function (resp) {
                      if (!resp.code) {
                          resp.items = resp.items || [];
                          this.setState({data: resp.items});
                      }
                  }.bind(this)
              );
          }
      }

  },
  handleRecordSubmit: function(notes) {
      if(google.appengine.hopster.diary.api_ready) {
          var token = sessionStorage.getItem('accessToken') || null;
          if (token) {
              google.appengine.hopster.diary.add(
                  notes,
                  token,
                  function (resp) {
                  }.bind(this)
              );
          }
      }

  },
  handleLoginSubmit: function(creditionals) {
      google.appengine.hopster.user.token (
          creditionals,
          function (resp) {
              if (!resp.code) {
                  resp.token = resp.token || null;
                  if(resp.token) {
                      sessionStorage.setItem('accessToken', resp.token);
                      this.setState({authComplete: true});
                  }
              }
          }.bind(this)
      );
  },
  getInitialState: function() {
    return {data: [], authComplete: false};
  },
  componentDidMount: function() {
    this.loadNotesFromServer();
    setInterval(this.loadNotesFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="recordBox">
        <h1>Records</h1>
        { !this.state.authComplete ? <LoginForm onLoginSubmit={this.handleLoginSubmit} /> : null }
        {  this.state.authComplete ? <RecordForm onRecordSubmit={this.handleRecordSubmit} /> : null }
        {  this.state.authComplete ? <RecordList data={this.state.data}/> : null }

      </div>
    );
  }
});

var RecordList = React.createClass({
  render: function() {
      var recordNodes = this.props.data.map(function(record) {
         return (
             <Record author={record.created} key={record.created}>
                 {record.notes}
             </Record>
         );
      });
    return (
      <div className="recordList">
          {recordNodes}
      </div>
    );
  }
});

var RecordForm = React.createClass({
  getInitialState: function() {
    return {notes: ''};
  },
  handleTextChange: function(e) {
    this.setState({notes: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var notes = this.state.notes.trim();
    if (!notes) {
      return;
    }
    this.props.onRecordSubmit({notes: notes});
    this.setState({notes: ''});
  },
  render: function() {
    return (
      <form className="recordForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Say something..."
          value={this.state.notes}
          onChange={this.handleTextChange}
        />
        <input type="submit" value="Post" />
      </form>
    );
  }
});

var Record = React.createClass({
  rawMarkup: function() {
    var md = new Remarkable();
    var rawMarkup = md.render(this.props.children.toString());
    return { __html: rawMarkup };
  },
  render: function() {
    var md = new Remarkable();
    return (
      <div className="record">
        <h2 className="recordAuthor">
          {this.props.author}
        </h2>
        <span dangerouslySetInnerHTML={this.rawMarkup()} />
      </div>
    );
  }
});

var LoginForm = React.createClass({
  getInitialState: function() {
    return {email: '', password: ''};
  },
  handleEmailChange: function(e) {
    this.setState({email: e.target.value});
  },
  handlePasswordChange: function(e) {
    this.setState({password: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var email = this.state.email.trim();
    var password = this.state.password;

    if (!email || !password) {
      return;
    }
    this.props.onLoginSubmit({email: email, password: password});
    this.setState({email: email, password: ''});
  },
  render: function() {
    return (
      <form className="loginForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Your email"
          value={this.state.email}
          onChange={this.handleEmailChange}
        />
        <input
          type="password"
          placeholder="Your password"
          value={this.state.password}
          onChange={this.handlePasswordChange}
        />

        <input type="submit" value="Login" />
      </form>
    );
  }
});

ReactDOM.render(
  <RecordBox pollInterval={2000} />,
  document.getElementById('content')
);
