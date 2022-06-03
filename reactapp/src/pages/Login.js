import React, { Component } from 'react';
import '../css/Login.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import Cookies from 'universal-cookie';

const baseUrl=process.env.REACT_APP_URL_BACKEND;
const cookies = new Cookies();

class Login extends Component {
    state={
        form:{
            email: '',
            password: ''
        }
    }

    handleChange=async e=>{
        await this.setState({
            form:{
                ...this.state.form,
                [e.target.name]: e.target.value
            }
        });
    }

    iniciarSesion=async()=>{
        
        try {
            let response = await axios.post(baseUrl+"api/token/", {email: this.state.form.email, password: this.state.form.password})
            if(response.data.access){
                cookies.set('access', response.data.access, {path: "/"});
                cookies.set('refresh', response.data.refresh, {path: "/"});
                window.location.href="./menu";
            }else{
                alert('El usuario o la contraseña no son correctos');
            }
        } catch (error) {
            console.log(error);
        }
        
    }

    componentDidMount() {
        if(cookies.get('access')){
           window.location.href="./menu";
        }
    }
    

    render() {
        return (
    <div className="containerPrincipal">
        <div className="containerSecundario">
          <div className="form-group">
            <label>Email: </label>
            <br />
            <input
              type="text"
              className="form-control"
              name="email"
              onChange={this.handleChange}
            />
            <br />
            <label>Contraseña: </label>
            <br />
            <input
              type="password"
              className="form-control"
              name="password"
              onChange={this.handleChange}
            />
            <br />
            <button className="btn btn-primary" onClick={()=> this.iniciarSesion()}>Iniciar Sesión</button>
          </div>
        </div>
      </div>
        );
    }
}

export default Login;