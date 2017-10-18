var login_name,login_password;
var user_list=[];
var isUser;
var user;
function login(){
	login_name=document.getElementById("logname").value;
	login_password=document.getElementById("logpass").value;
	//alert("username:"+login_name+"userpassword:"+login_password);
	isUser=checkUser();
    if(isUser=="no"){
        alert("no user");
    }else{
        self.location='hello';
    }
}

function checkUser(){
	getUser();
	for(var i=0;i<user_list.length;i++){
		if(login_name==user_list[i].uname&&login_password==user_list[i].upassword){
			user=user_list[i];
			return user;
		}else{
		    return 'no';
		}
	}
}


function getUser(){
	$.ajax({
		type : "GET",
		async : false,
		dataType : "json",
		url : "/getuserdb",
		data : {},
		success : function(msg) {
		
			var json = msg;
			user_list = json;
		}
	});
}