// TODO:
//    - pagination of TopicTitleList with links
//    - icons
//    - answer/edit forms (add API)
//    - search form (add API)
//    - i18n (date)
//    etc.

moment.locale('fr');

var Message = React.createClass({
  rawMarkup: function() {
    var md = new Remarkable('full');
    var rawMarkup = md.render(this.props.data.text.toString());
    return { __html: rawMarkup };
  },
  render: function() {
    var m = moment(this.props.data.pub_date);
    var dateStr = m.fromNow();
    var message = this.props.data;
    return (
      <div className="message">
        <h3>
          <img src={'/static/forum/icons/'+message.icon.filename} alt={message.icon.filename} />
          {' '}
          {message.title}
          <small>
            {' par '}
            <strong>
              {message.author.username}
            </strong>
            {' '}
            {dateStr}
          </small>
        </h3>
        <div className="well well-sm forum-text" dangerouslySetInnerHTML={this.rawMarkup()} />
      </div>
    );
  }
});

var TopicTitle = React.createClass({
  render: function() {
    return (
      <div className="topic">
        <h2>
          {this.props.title} <small>{this.props.author}</small>
        </h2>
      </div>
    );
  }
});

var TopicTitleList = React.createClass({
  getInitialState: function() {
    return {topics: []};
  },
  componentDidMount: function() {
    this.loadTopicListFromServer();
    setInterval(this.loadTopicListFromServer, this.props.pollInterval);
  },
  loadTopicListFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({topics: data.results});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var topicNodes = this.state.topics.map(function(topic) {
      // return ( <TopicTitle key={topic.pk} author={topic.author.username} title={topic.title} />);
      return( <TopicMessageList key={topic.pk} url={topic.url} pollInterval={30000} /> );
    });
    return (
      <div className="topicList">
        {topicNodes}
      </div>
    );
  }
});

var TopicMessageList = React.createClass({
  getInitialState: function() {
    return {messages: []};
  },
  componentDidMount: function() {
    this.loadMessagesListFromServer();
    setInterval(this.loadMessagesListFromServer, this.props.pollInterval);
  },
  loadMessagesListFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({messages: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getAnswers: function(message, messageSet) {
    var self = this;
    var answerSet = new Set();
    for (let item of messageSet.values()) {
      if ((item.question == null) || (message.pk == item.pk))
        messageSet.delete(item);
      else if (item.question.pk == message.pk) {
        answerSet.add(item);
        messageSet.delete(item);
      }
    }
    if (answerSet.size == 0) return null;
    var answerNodes = new Array();
    answerSet.forEach(function(a) {
      var aAnswerNodes = self.getAnswers(a, messageSet);
      answerNodes.push(
        <li key={a.pk} className="answer rborder children">
          <Message data={a} />
           <ul className="answers children">
            {aAnswerNodes}
           </ul>
        </li>
      );
    });
    return answerNodes;
  },
  render: function() {
    if (this.state.messages.length == 0) return null;
    var rootMessage = this.state.messages[0];
    var rootAnswers = this.getAnswers(rootMessage, new Set(this.state.messages));
    return (
      <ul className="answers root">
        <li className="answers root">
          <Message data={rootMessage} />
          <ul className="answers children">
            {rootAnswers} 
          </ul>
        </li>
      </ul>
    );
  }
});

ReactDOM.render(
  <TopicTitleList url="/api/topics/" pollInterval={10000} />,
  document.getElementById('content')
);
