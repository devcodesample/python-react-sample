import React, { useCallback } from 'react';
import { Link } from 'react-router-dom';
import Toggle from 'react-toggle';
import Dropzone from 'react-dropzone'
import { useForm, Controller } from "react-hook-form";
// noinspection NpmUsedModulesInstalled
import { connect } from 'react-redux'
import { useTranslation } from "react-i18next";
import avatar33 from '../../../images/avatars/33.jpg'
import { userActions } from '../../../_actions/users'
import {
    Container,
    Row,
    Col,
    Card,
    CardBody,
    Button,
    Form,
    FormGroup,
    Label,
    Input,
    FormText
}
    from '../../../components';
function Profile(props) {

    // noinspection JSUnusedLocalSymbols
    const { handleSubmit, control, errors, register } = useForm({
        mode: "onChange",
        reValidateMode: "onChange",
    });
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles != null) {
            acceptedFiles.forEach((file) => {
                props.updateProfilePic(file, props.user.profile.id)
            })
        }
    }, [])

// noinspection JSUnusedLocalSymbols
    const { t } = useTranslation();
    const handleProfileUpdate = (data) => {
        props.updateUserDetails(data, props.user.id, props.user.profile.id)
    }
    // noinspection SpellCheckingInspection
    return (
        <React.Fragment>
            <Container fluid>
                <Card className="main-header p-3">
                    <Row>
                        <Col className="float-left" lg={6}>
                            <div>
                                <span> <Link to="/settings"><i className="fa fa-cog mr-1" aria-hidden="true"/>Settings </Link></span>
                                <span><i className="fa fa-chevron-right mr-2 ml-2" aria-hidden="true"/>Your Profile</span>
                            </div>
                        </Col>
                        <Col className="float-right" lg={6}>
                            <div>
                                <Link to="/change-password">
                                    <Button type="submit" color="light" className=" float-right">
                                        <i className="fa fa-key mr-2" aria-hidden="true"/>Change Password</Button>
                                </Link>
                            </div>
                        </Col>
                    </Row>
                </Card>
            </Container>

            <Container>
                <div className="text-center mb-4 pro_sec ">
                    <img src={props.user.profile.profile_photo ? props.user.profile.profile_photo.replace(/\?.*/, '') : avatar33} className="avatar_img av_pro" alt="profile_photo"/>
                    <h2 className="mb-4">You Profile</h2>
                </div>

                <Row>
                    <Col lg={6}>
                        <h4>Your Photo</h4>
                        <p>Upload a photo to make follow-up messages to customers – and your notes to colleagues – more personal.</p>
                    </Col>
                    <Col lg={6}>
                        <Card className="choose_file border_left_card">
                            <CardBody>
                                <div className="text-center mb-4">
                                    <img src={props.user.profile.profile_photo ? props.user.profile.profile_photo.replace(/\?.*/, '') : avatar33} className="avatar_img av_pro" alt="avatar"/>
                                    <p className="mb-4">To upload a new photo</p>
                                </div>

                                <Dropzone onDrop={onDrop} multiple={false}>
                                    {({ getRootProps, getInputProps }) => (
                                        <section>
                                            <div {...getRootProps()} className={"dropzone"}>
                                                <i className="fa fa-cloud-upload fa-fw fa-3x mb-3"/>
                                                <input {...getInputProps()} />
                                                <h5 className='mt-0'>
                                                    Drag & Drop or click to upload
                                               </h5>
                                            </div>
                                        </section>
                                    )}
                                </Dropzone>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>

                { /* START Section 1 */}
                { /* START Form */}
                <Form onSubmit={handleSubmit(handleProfileUpdate)}>
                    <Row>
                        <Col lg={6}>
                            <h4>Your Info</h4>
                            <p>The Basic - name, email, Job title.
             </p>
                        </Col>
                        <Col lg={6}>
                            <Card className="border_left_card">
                                <CardBody>
                                    { /* START Input */}
                                    <Col lg={12}>
                                        <FormGroup>
                                            <Label for="first_name">First Name</Label>
                                            <Controller
                                                as={<Input />}
                                                type="text"
                                                name="first_name"
                                                id="first_name"
                                                placeholder="First Name..."

                                                control={control}
                                                rules={{
                                                    required: {
                                                        value: true,
                                                        message: "first name is required field.",
                                                    },
                                                    pattern: {
                                                        value: /^[A-Za-z]+$/,
                                                        message: "first name must be alphabetic characters.",
                                                    },
                                                    maxLength: {
                                                        value: 50,
                                                        message: "first name must not be greater than 50 characters.",
                                                    },
                                                    minLength: {
                                                        value: 2,
                                                        message: "first name must be at least 2 characters.",
                                                    },
                                                }}
                                                defaultValue={props.user.first_name}

                                            />
                                            {errors.first_name && (
                                                <FormText color={"danger"} >{errors.first_name.message} </FormText>
                                            )}
                                        </FormGroup>
                                    </Col>
                                    { /* END Input */}
                                    { /* START Input */}
                                    <Col lg={12}>
                                        <FormGroup>
                                            <Label for="username">Last Name</Label>
                                            <Controller
                                                as={<Input />}
                                                type="text"
                                                name="last_name"
                                                id="last_name"
                                                placeholder="Last Name..."

                                                control={control}
                                                rules={{
                                                    required: {
                                                        value: true,
                                                        message: "last name is required field.",
                                                    },
                                                    pattern: {
                                                        value: /^[A-Za-z]+$/,
                                                        message: "last name must be alphabetic characters.",
                                                    },
                                                    maxLength: {
                                                        value: 50,
                                                        message: "last name must not be greater than 50 characters.",
                                                    },
                                                    minLength: {
                                                        value: 2,
                                                        message: "last name must be at least 2 characters.",
                                                    },
                                                }}
                                                defaultValue={props.user.last_name}

                                            />
                                            {errors.last_name && (
                                                <FormText color={"danger"} >{errors.last_name.message} </FormText>
                                            )}
                                        </FormGroup>
                                    </Col>
                                    { /* END Input */}
                                    { /* START Input */}
                                    <Col lg={12}>
                                        <FormGroup>
                                            <Label for="repeatPassword">Email Address</Label>
                                            <Controller
                                                as={<Input />}
                                                name="email"
                                                id="emailAdress"
                                                control={control}
                                                type={"email"}
                                                placeholder="Email Address..."

                                                defaultValue={props.user.email}
                                                rules={{
                                                    required: {
                                                        value: true,
                                                        message: "email address is required field.",
                                                    },
                                                    pattern: {
                                                        value: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
                                                        message: "invalid email address"
                                                    }
                                                }}

                                            />
                                            {errors.email && (
                                                <FormText color={"danger"}>{errors.email.message} </FormText>
                                            )}
                                        </FormGroup>
                                    </Col>
                                    { /* END Input */}
                                    { /* START Input */}
                                    <Col lg={12}>
                                        <FormGroup>
                                            <Label for="job_title">
                                                Job Title
                                            </Label>
                                            <Controller
                                                as={<Input />}
                                                name={"job_title"}
                                                control={control}
                                                id="job_title"
                                                placeholder="Job Title..."
                                                defaultValue={props.user.profile.job_title}
                                                rules={{
                                                    required: {
                                                        value: true,
                                                        message: "job title is required field.",
                                                    },
                                                    maxLength: {
                                                        value: 50,
                                                        message:
                                                            "job title must not be greater than 50 characters.",
                                                    },
                                                }}

                                            />
                                            {errors.name && (
                                                <FormText>
                                                    {errors.name.message}
                                                </FormText>
                                            )}
                                        </FormGroup>
                                    </Col>
                                    { /* END Input */}

                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                    { /* END Section 1 */}


                    <Row>
                        <Col lg={6}>
                            <h4>Notification Settings</h4>
                            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. </p>
                        </Col>
                        <Col lg={6}>
                            <Card className=" notifi_setting border_left_card">
                                <CardBody>
                                    <div className="weekly-summary">
                                        <label>
                                            <strong className="text-left mb-4">Weekly Summary</strong>
                                            <p className="mt-2 "> Send me a weekly summary email when there is activity
                        to report (new survey responses, messages, or notes). </p>
                                        </label>
                                        <div className="custom-toggle">
                                            <Toggle icons={false} />
                                        </div>
                                    </div>

                                    <div className="weekly-summary1 mb-4">
                                        <label>
                                            <strong className="text-left mb-4">Message & Assignment Notifications</strong>
                                            <p className="mt-2">Send me an email notification when customers respond to my
                        follow-up messages or when survey responses are assigned to me.</p>
                                        </label>
                                        <div className="custom-toggle">
                                            <Toggle icons={false} />
                                        </div>
                                    </div>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={6}>
                            <h4>User Role </h4>
                            <p>SurveyMonkey CX currently features 4 different user roles: Admin, Contributor, Analyst, and Viewer. The four user roles have different
             permission levels and allow you to take certain actions. Read more about user roles.</p>

                        </Col>
                        <Col lg={6}>
                            <Card className=" notifi_setting border_left_card">
                                <CardBody>
                                    <p className="text-center"><strong>Your role :</strong></p>
                                    <p className="m-0">Think you need a different role?</p>
                                    <p> Contact your account owner:
                          <Link to="!#">Lisa Brown</Link></p>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>


                    <Row>
                        <Col lg={6}>
                            <h4>Your stats</h4>
                            <p>Your list of stats showing the actions you’ve taken in SurveyMonkey CX</p>
                        </Col>
                        <Col lg={6}>
                            <Card className="mb-0 boxes border_left_card no_margin">
                                <CardBody>
                                    <Col lg={6} className="b_sec float-left">
                                        <h5>6</h5>
                                        <p>Surveys Created</p>
                                    </Col>

                                    <Col lg={6} className="b_sec float-left">
                                        <h5>Aug. 4, 2020</h5>
                                        <p>Last Active</p>
                                    </Col>
                                    <Col lg={6} className="b_sec float-left">
                                        <h5>0</h5>
                                        <p>Open Survey Responses</p>
                                    </Col>

                                    <Col lg={6} className="b_sec float-left">
                                        <h5>0</h5>
                                        <p>Closed Survey Responses</p>
                                    </Col>
                                    <Col lg={6} className="b_sec float-left">
                                        <h5>0</h5>
                                        <p>Message Send</p>
                                    </Col>

                                    <Col lg={6} className="b_sec float-left" >
                                        <h5>3</h5>
                                        <p>Internal Notes</p>
                                    </Col>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>

                    <Button color="primary" className="setting_btn float-right mb-4">
                        SAVE & CHANGE
                  </Button>
                </Form>
                { /* END Form */}
            </Container>
        </React.Fragment>
    )
}

const mapStateToProps = (state) => {
    return {
        user: state.authentication.user
    }
}
const actionCreators = {
    updateProfilePic: userActions.updateProfilePic,
    updateUserDetails: userActions.updateUserDetails,
};
const connectProfile = React.memo(connect(mapStateToProps, actionCreators)(Profile))
export { connectProfile as Profile };
