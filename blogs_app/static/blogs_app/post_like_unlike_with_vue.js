var postDetail = new Vue({
  el: '#likeComment',
  delimiters: ['[[', ']]'],

  data: {
    //captures context data here
    likeStatus: '{{like_status}}',
    userId: '{{user.id}}',
    postId: '{{post.id}}',
    postLikes: '{{post_likes}}',
    commentsList: '{{comments_list}}',
    currentComment:'',
    
  },

  methods: {
    likeUnlikePost() {

      var data = {
        'userId': this.userId,
        'postId': this.postId,
        'likeStatus': this.likeStatus,
      };

      fetch('/api/like', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
          },
          credentials: 'same-origin',
          body: JSON.stringify(data)
        })

        //'async and await' keywords are required to resolve promises
        // need to clear your concept on async, await and promises 
        .then(async response => {
          const data = await response.json();
          console.log(data);
          this.likeStatus = data['likeStatus'];
          this.postLikes = data['post_likes'];

        })
        .catch(function (error) {
          console.log(error);
        })
    },

    addUpComment(){
      //Problem needs to be solved with this function
      var data = {
        'userId': this.userId,
        'postId': this.postId,
        'comment': this.currentComment
      };

      fetch('/api/comment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
          },
          credentials: 'same-origin',
          body: JSON.stringify(data)
        })

        //'async and await' keywords are required to resolve promises
        // need to clear your concept on async, await and promises 
        .then(async response => {
          const data = await response.json();
          //The returned response contains id only in place of user and
          //post objects
          console.log(data);
          this.currentComment = '';

        })
        .catch(function (error) {
          console.log(error);
        })
    },

  },

})