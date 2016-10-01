// TODO:
//    - routes to topics and messages
//    - answer/edit forms (add API)
//    - search form (add API)
//    - i18n (date)
//    etc.

var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');
var Remarkable = require('remarkable');

var moment = require('moment');
require('moment/locale/fr');
// moment.locale('fr');

function getParameterByName(name, url) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(url)||[,""])[1].replace(/\+/g, '%20'))||null;
}

var Message = React.createClass({
  rawMarkup: function() {
    var md = new Remarkable('full');
    var rawMarkup = md.render(this.props.message.text.toString());
    return { __html: rawMarkup };
  },
  render: function() {
    var message = this.props.message;
    return (
      <div className="message">
        <MessageTitle icon={message.icon} title={message.title} author={message.author} pub_date={message.pub_date} />
        <div className="forum-text" dangerouslySetInnerHTML={this.rawMarkup()} />
      </div>
    );
  }
});

var MessageTitle = React.createClass({
  render: function() {
    var dateStr = moment(this.props.pub_date).fromNow();
    return (
      <h4 className="messageTitle">
        <img src={'/static/forum/icons/'+this.props.icon.filename} alt={this.props.icon.filename} />
        {' '}
        {this.props.title}
        <small>
          {' par '} <strong> {this.props.author.username} </strong> {' '} {dateStr}
        </small>
      </h4>
    );
  }
});

var TopicList = React.createClass({
  getInitialState: function() {
    return {
      url: '/api/topics/?page=1',
      next: null,
      previous: null,
      topics: [],
      loadInterval: null
    };
  },
  componentDidMount: function() {
    this.loadTopicListFromServer();
    var id = setInterval(this.loadTopicListFromServer, this.props.pollInterval);
    this.setState({loadInterval: id});
  },
  componentWillUnmount: function() {
    if (this.state.loadInterval == null) return;
    clearInterval(this.state.loadInterval);
    this.setState({loadInterval: null});
  },
  loadTopicListFromServer: function() {
    $.ajax({
      url: this.state.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({
          url: this.state.url,
          next: data.next,
          previous: data.previous,
          topics: data.results
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  previousClick: function(e) {
    e.preventDefault();
    if (this.state.previous == null) return
    this.setState(
      {
        next: this.state.url,
        url: this.state.previous,
      },
      this.loadTopicListFromServer
    );
  },
  nextClick: function(e) {
    e.preventDefault();
    if (this.state.next == null) return
    this.setState(
      {
        previous: this.state.url,
        url: this.state.next,
      },
      this.loadTopicListFromServer
    );
  },
  render: function() {
    var page = getParameterByName('page', this.state.url)||1;
    var topicNodes = this.state.topics.map(function(topic) {
      return( <MessageTree key={topic.pk} url={topic.url} pollInterval={30000} /> );
    });
    var navBar = 
        <nav className="text-center">
          <ul className="pagination">
            <li className={this.state.previous ? "" : "disabled"}><a href="#" onClick={this.previousClick} aria-label="Précédent"><span aria-hidden="true">«</span></a></li>
            <li className="active"><a href="#">{page + ' '}<span className="sr-only">(current)</span></a></li>
            <li className={this.state.next ? "" : "disabled"}><a href="#" onClick={this.nextClick} aria-label="Suivant"><span aria-hidden="true">»</span></a></li>
          </ul>
        </nav>;
    return (
      <div className="topicList">
        {navBar}
        {topicNodes}
        {navBar}
      </div>
    );
  }
});

var MessageTree = React.createClass({
  getInitialState: function() {
    return {
      messages: [],
      loadInterval: null
    };
  },
  componentDidMount: function() {
    this.loadMessagesListFromServer();
    var id = setInterval(this.loadMessagesListFromServer, this.props.pollInterval);
    this.setState({loadInterval: id});
  },
  componentWillUnmount: function() {
    if (this.state.loadInterval == null) return;
    clearInterval(this.state.loadInterval);
    this.setState({loadInterval: null});
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
  getAnswerNodes: function(message, messageSet) {
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
      if (a.is_leaf_node)
        var answerList = null;
      else {
        var aAnswerNodes = self.getAnswerNodes(a, messageSet);
        var answerList = <AnswerList> {aAnswerNodes} </AnswerList>;
      }
      answerNodes.push(
        <li key={a.pk} className="well well-sm rborder">
          <Message message={a} />
          {answerList}
        </li>
      );
    });
    return answerNodes;
  },
  render: function() {
    if (this.state.messages.length == 0) return null;
    var rootMessage = this.state.messages[0];
    if (rootMessage.is_leaf_node)
      var answerList = null;
    else {
      var rootAnswers = this.getAnswerNodes(rootMessage, new Set(this.state.messages));
      var answerList = <AnswerList> {rootAnswers} </AnswerList>;
    }
    return (
      <ul className="topic">
        <li className="well well-sm">
          <Message message={rootMessage} />
          {answerList}
        </li>
      </ul>
    );
  }
});

var AnswerList = React.createClass({
  getInitialState: function () {
    return { hidden: false, };
  },
  handleClick: function (e) {
    e.preventDefault();
    this.setState({hidden: !this.state.hidden});
  },
  render: function() {
    if (this.state.hidden) {
      var str = 'montrer les réponses';
      var style = {display: 'none'};
    } else {
      var str = 'cacher les réponses';
      var style = {display: 'unset'};
    }
    return (
      <div className="answerList">
        <a href="#" onClick={this.handleClick}>{'['+str+']'}</a>
        <ul style={style} className="answers">
          {this.props.children}
        </ul>
      </div>
    );
  }
});

ReactDOM.render(
  <TopicList pollInterval={10000} />,
  document.getElementById('content')
);
