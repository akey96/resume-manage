import React, { Component } from 'react';
import Cookies from 'universal-cookie';
import axios from 'axios';
import '../css/Menu.css';
import "bootstrap/dist/css/bootstrap.min.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilePdf, faFileText } from '@fortawesome/free-solid-svg-icons';

const cookies = new Cookies();
const baseUrl=process.env.REACT_APP_URL_BACKEND;

class Menu extends Component {

    state = {
        data: [],
        form: {
            id: '',
            nombre: '',
            pais: '',
            capital_bursatil: '',
            tipoModal: ''
        }
    }
    

    async downloadPDF(profile) {
        console.log(profile);
        axios({
            url: `${baseUrl}resumes/${profile.id}.pdf`,
            method: 'GET',
            responseType: 'blob',
            headers: { Authorization: `Bearer ${cookies.get('access')}`} 
          }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${profile.first_name} ${profile.last_name}.pdf`);
            document.body.appendChild(link);
            link.click();
          });
    }

    async downloadMD(profile) {
        console.log(profile);
        axios({
            url: `${baseUrl}resumes/${profile.id}.md`,
            method: 'GET',
            responseType: 'blob',
            headers: { Authorization: `Bearer ${cookies.get('access')}`} 
          }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${profile.first_name} ${profile.last_name}.md`);
            document.body.appendChild(link);
            link.click();
          });
    }


    handleChange = async e => {
        e.persist();
        await this.setState({
            form: {
                ...this.state.form,
                [e.target.name]: e.target.value
            }
        });
        console.log(this.state.form);
    }

    cerrarSesion = () => {
        cookies.remove('access');
        cookies.remove('refresh');
        window.location.href = './';
    }

    async componentDidMount() {
        console.log(`Este!!   ${process.env.REACT_APP_URL_BACKEND}`)
        if (!cookies.get('access')) {
            window.location.href = "./";
        } else {
            try {
                var response = await axios.post(baseUrl + "api/token/verify/", { token: cookies.get('access') });
                console.log(`verify  ${response}`);
            } catch (error) {
                console.error(`verify error ${error}`);
                window.location.href = "./";
                try {
                    var refresh = await axios.post(baseUrl + "api/token/refresh/", { refresh: cookies.get('refresh') });
                    cookies.set('access', refresh.data.access, { path: "/" });
                    console.log(`refresh  ${refresh}`);
                } catch (erro) {
                    console.error(`refresh error ${erro}`);
                    window.location.href = "./";
                }
            }
            try {
                let profiles = await axios.get(baseUrl + "resumes/profile", { headers: { Authorization: `Bearer ${cookies.get('access')}`} });
                this.state.data = profiles.data;
                await this.setState({
                    form: {
                        ...this.state.form,
                    }
                });
                
            } catch (error_profile) {
                console.error(error_profile);
            }
            
        }

    }

    render() {
        return (
        
            <div className="contanierprincipal">

                <nav class="navbar navbar-dark bg-dark">
                    <div class="container-fluid">
                        <a class="navbar-brand">Resume Manager</a>
                        <button class="btn btn-outline-info" onClick={() => { this.cerrarSesion()}}>Salir</button>

                    </div>
                </nav>

                <br /><br />
                <div class="row">
                    <div class="col-md-1"></div>
                    <div class="col-md-10">
                        <table className="table">
                            <thead>
                                <tr>
                                    {/* <th>ID</th> */}
                                    <th>Nombre</th>
                                    <th>Apellido</th>
                                    <th>Celular</th>
                                    <th>Email</th>
                                    <th>git</th>
                                    <th>Descargar</th>
                                </tr>
                            </thead>
                            <tbody class="table-group-divider">
                                
                                {this.state.data.map(profile => {
                                    return (
                                        <tr>
                                            {/* <td>{profile.id}</td> */}
                                            <td>{profile.first_name}</td>
                                            <td>{profile.last_name}</td>
                                            <td>{profile.phone}</td>
                                            <td>{profile.email}</td>
                                            <td>{profile.git}</td>
                                            <td>
                                                <button className="btn btn-primary" onClick={() => { this.downloadPDF(profile)}}><FontAwesomeIcon icon={faFilePdf} /></button>
                                                {"   "}
                                                <button className="btn btn-danger" onClick={() => { this.downloadMD(profile) }}><FontAwesomeIcon icon={faFileText} /></button>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                    <div class="col-md-1"></div>
                </div>
                
            </div>

        );
    }
}

export default Menu;