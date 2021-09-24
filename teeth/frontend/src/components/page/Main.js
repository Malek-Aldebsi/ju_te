import React, { Component, Fragment, useRef } from 'react'
import { connect } from 'react-redux'
import { upload, delete_current, download } from '../../actions/engine'
import { Field, Form, Formik } from 'formik'
import { Box, Center, HStack, List } from '@chakra-ui/layout'
import { FormControl, FormLabel } from '@chakra-ui/form-control'
import { Select } from '@chakra-ui/select'
import { Input, InputGroup, InputRightElement } from '@chakra-ui/input'
import { Image } from '@chakra-ui/image'
import { Button } from '@chakra-ui/button'
import { Spinner } from '@chakra-ui/spinner'
import { useRecoilState } from 'recoil'
import { engineState } from '../../states'
import { UnorderedList, ListItem } from '@chakra-ui/layout'

export default function Main () {}

function ToothForm () {
  const photoRef = useRef()
  const aspectOptions = [
    {
      label: 'type 1',
      value: 'type 1'
    },
    {
      label: 'Others',
      value: 'Others'
    }
  ]

  const angleOptions = [
    {
      label: 'Labial',
      value: 'Labial'
    },
    {
      label: 'Lingual',
      value: 'Lingual'
    },
    {
      label: 'Mesial',
      value: 'Mesial'
    },
    {
      label: 'Destial',
      value: 'Destial'
    },
    {
      label: 'top view',
      value: 'top view'
    }
  ]

  const initialValues = {
    aspect: '',
    angle: '',
    file: null
  }
  const onSubmit = values => {
    console.log(values)
    alert('submitted successfully')
  }

  return (
    <Box m={[2, 4, 12]} p={6}>
      <Formik initialValues={initialValues} onSubmit={onSubmit}>
        <Form>
          <Field name='aspect'>
            {({ field, form }) => (
              <FormControl isRequired mb={3}>
                <FormLabel htmlFor='aspect'>Photo Aspect</FormLabel>
                <Select {...field}>
                  {aspectOptions.map((item, idx) => (
                    <option key={idx} value={item.value}>
                      {item.label}
                    </option>
                  ))}
                </Select>
              </FormControl>
            )}
          </Field>
          <Field name='angle'>
            {({ field, form }) => (
              <FormControl isRequired mb={3}>
                <FormLabel htmlFor='angle'>Photo angle</FormLabel>
                <Select {...field}>
                  {angleOptions.map((item, idx) => (
                    <option key={idx} value={item.value}>
                      {item.label}
                    </option>
                  ))}
                </Select>
              </FormControl>
            )}
          </Field>
          <Field name='file'>
            {({ field, form }) => (
              <FormControl isRequired mb={3}>
                <FormLabel htmlFor='angle'>Tooth Photo</FormLabel>
                <Input
                  type='file'
                  display='none'
                  onChange={e =>
                    form.setFieldValue('file', e.currentTarget.files[0])
                  }
                  ref={photoRef}
                />
                <InputGroup>
                  <Input
                    isReadOnly
                    value={field?.value?.name || 'Upload a Photo'}
                  />

                  <InputRightElement w='30%'>
                    <Button
                      w='100%'
                      colorScheme='blue'
                      onClick={() => photoRef.current.click()}
                    >
                      Upload
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>
            )}
          </Field>
          <Button type='submit'>Submit</Button>
        </Form>
      </Formik>
    </Box>
  )
}

function Loading () {
  return (
    <Center>
      <Spinner size='xl' />
    </Center>
  )
}

function Result () {
  const [engineObject, setEngineObject] = useRecoilState(engineState)
  return (
    <Box>
      <Image
        src={this.props.assessment.processed_image}
        width='100%'
        maxH='800px'
      />
      <UnorderedList>
        {engineObject.assessment.notes.map((note, idx) => (
          <ListItem key={idx}>note</ListItem>
        ))}
      </UnorderedList>

      <HStack w='100%' justify='space-between' spacing={6}>
        <Button>ReSubmit Another</Button>
        <Button
          onClick={() =>
            fetch(
              `engine/api/assessments/${engineObject.assessment.id}/report/`
            )
          }
        >
          Save
        </Button>
      </HStack>
    </Box>
  )
}

// class Main extends Component {
//   constructor (props) {
//     super(props)
//     this.fileInput = React.createRef()
//   }

//   state = {
//     aspect: 'Labial',
//     type: 'type 1'
//   }

//   componentDidUpdate () {
//     //this.props.delete_current(false);
//   }

//   handleChange = event => {
//     this.setState({ [event.target.name]: event.target.value })
//   }

//   handleSubmit = event => {
//     event.preventDefault()
//     const { aspect, type } = this.state
//     this.props.upload({
//       aspect,
//       type,
//       image: this.fileInput.current.files[0]
//     })
//   }

//   render () {
//     let body = <div></div>

//     if (this.props.isLoading) {
//       body = (
//         <div className='card-body mt-5 text-center'>
//           <h6 className='h6'>Loading</h6>
//           <div className='spinner-border text-muted' role='status'>
//             <span className='visually-hidden'>Loading...</span>
//           </div>
//         </div>
//       )
//     } else if (this.props.assessment) {
//       const notes = this.props.assessment.notes.map((note, id) => (
//         <li key={id} className='list-group-item'>
//           {note.note}
//         </li>
//       ))
//       body = (
//         <Fragment>
//           <img
//             className='img-fluid'
//             src={this.props.assessment.processed_image}
//             style={{ maxHeight: '1000px', width: '100%' }}
//           ></img>
//           <div className='card-body'>
//             <ul className='list-group list-group-flush'>{notes}</ul>

//             <button
//               type='button'
//               className='btn btn-primary'
//               onClick={() => this.props.delete_current(true)}
//             >
//               ReSubmit Another
//             </button>

//             <a
//               className='btn btn-primary ms-1'
//               href={`engine/api/assessments/${this.props.assessment.id}/report/`}
//             >
//               Save
//             </a>
//           </div>
//         </Fragment>
//       )
//     } else {
//       body = (
//         <div className='card-body'>
//           <form
//             className='row justify-content-center'
//             encType='multipart/form-data'
//             onSubmit={this.handleSubmit}
//           >
//             <div className='mb-3 col-xs-12 col-md-6'>
//               <label className='form-label' htmlFor='type'>
//                 Photo Type
//               </label>
//               <select
//                 className='form-select'
//                 name='type'
//                 value={this.state.type}
//                 onChange={this.handleChange}
//               >
//                 <option value='type 1'>type 1</option>
//                 <option value='Others'>Others</option>
//               </select>
//             </div>

//             <div className='w-100' />

//             <div className='mb-3 col-xs-12 col-md-6'>
//               <label className='form-label' htmlFor='aspect'>
//                 Photo Aspect
//               </label>

//               <select
//                 className='form-select'
//                 name='aspect'
//                 value={this.state.aspect}
//                 onChange={this.handleChange}
//                 required
//               >
//                 <option value='Labial'>Labial</option>
//                 <option value='Lingual'>Lingual</option>
//                 <option value='Mesial'>Mesial</option>
//                 <option value='Destial'>Destial</option>
//                 <option value='top view'>top view</option>
//               </select>
//             </div>

//             <div className='w-100' />

//             <div className='mb-3 col-xs-12 col-md-6'>
//               <label htmlFor='file' className='form-label'>
//                 Tooth Photo
//               </label>
//               <input
//                 className='form-control'
//                 type='file'
//                 name='file'
//                 ref={this.fileInput}
//                 required
//               />
//             </div>

//             <div className='w-100'></div>

//             <button
//               type='submit'
//               className='btn btn-primary btn-block mb-4 col-xs-8 col-sm-6 col-md-2'
//             >
//               Submit
//             </button>
//           </form>
//         </div>
//       )
//     }

//     return (
//       <div className='container'>
//         <div className='row justify-content-center mt-5'>
//           <div className='col-xs-12 col-md-6'>
//             <div className='card h-100' style={{ maxHeight: '8rm' }}>
//               <div className='card-header'>
//                 <h4 className='h4'>Tooth Picture</h4>
//               </div>
//               {body}
//             </div>
//           </div>
//         </div>
//       </div>
//     )
//   }
// }

// const mapStateToProps = state => ({
//   isLoading: state.engine.isLoading,
//   assessment: state.engine.assessment
// })

// export default connect(mapStateToProps, { upload, delete_current, download })(
//   Main
// )
