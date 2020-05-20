import React from 'react';
import rp from 'request-promise';
import {
  H3, ProgressBar, Dialog, InputGroup, Classes, Button, Colors, Intent, FormGroup, Tooltip, Icon, H5,
} from '@blueprintjs/core';
import { withStyles, makeStyles, createStyles } from '@material-ui/styles';
import { Theme, WithStyles, Paper, Grid, Typography } from '@material-ui/core';
import blue from '@material-ui/core/colors/blue';

import Message, { TIMEOUT } from 'utils/Message';
import 'styles/QKTView.css';


const { REACT_APP_QKT_HOST = 'localhost', REACT_APP_QKT_PORT = 5000 } = process.env;
const ENDPOINT = `http://${REACT_APP_QKT_HOST}:${REACT_APP_QKT_PORT}`;
const TILE_COLOR = blue[500];

const styles = (theme: Theme) => createStyles({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 50,
    width: 50,
    justifyContent: 'center',
    display: 'flex',
    flexDirection: 'column',
  },
});

enum Stage {
  Solving,
  Finished,
}

interface AlphaValidation {
  valid: boolean;
  alpha: number[] | null;
}

interface Props extends WithStyles<typeof styles> { }

interface State {
  stage: Stage;
  alpha: number[] | null;
  T: number[][] | null;
  status: string | null;
  numSolutions: number | null;
  validAlphaText: boolean;
  alphaText: string;
}

/**
 * There a 3 stages:
 *   1. Inform the user what they need to do.
 *   2. Retrieval and display of QKTs.
 *   3. Show info after done.
 */

class QKTView extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      stage: Stage.Finished,
      alpha: null,
      status: null,
      numSolutions: null,
      T: null,
      validAlphaText: false,
      alphaText: '',
    };
  }

  componentDidMount = () => { };

  componentWillUnmount = () => { };

  doneSolving = () => {
    this.setState({
      stage: Stage.Finished,
    });
  };

  buildGrid = (grid: number[][]) => {
    const { classes } = this.props;

    return (
      <Grid container className={classes.root}>
        <Grid item xs='auto'>{grid.map((row, r) => (
          <Grid container className={classes.root} key={r} spacing={0}>{row.map((value, c) => (
            <Grid item key={`${r}.${c}`}>
              <Paper
                className={classes.paper}
                style={{ backgroundColor: TILE_COLOR }}>
                  <Typography>
                    {value}
                  </Typography>
                </Paper>
            </Grid>
          ))}</Grid>
        ))}</Grid>
      </Grid>
    );
  };


  /**
   * The alpha text is valid if it:
   *   - is non-empty,
   *   - is a list of positive integers delimited by commas.
   */
  validateAlphaText = (text: string): AlphaValidation => {
    const notValid = { valid: false, alpha: null };

    if (text.trim() === '') return notValid;

    const arr = text.split(/[ \t,]+/);
    if (!arr.every(x => Number.isInteger(+x))) return notValid;

    const alpha = arr
      .filter(x => x !== '')
      .map(x => Number.parseInt(x));
    if (alpha.length == 0) return notValid;
    if (alpha.some(x => x < 0)) return notValid;

    return { valid: true, alpha };
  };

  sendRequest = async (alpha: number[]) => {
    const options: rp.OptionsWithUrl = {
      url: `${ENDPOINT}/solve`,
      useQuerystring: true,
      qs: {
        'alpha[]': alpha,
      },
      json: true,
    };

    let response = null;
    try {
      response = await rp(options);
    } catch (e) {
      Message.show({
        timeout: TIMEOUT,
        message: `Unable to solve: ${e}`,
        icon: 'warning-sign',
        intent: Intent.DANGER,
      });
      return this.setState({ stage: Stage.Finished });
    }

    Message.show({
      timeout: TIMEOUT,
      message: 'Successfully solved',
      icon: 'tick',
      intent: Intent.SUCCESS,
    });
    return this.setState({
      stage: Stage.Finished,
      numSolutions: response['num_solutions'],
      status: response['status'],
      T: response['sample_solution'],
      alpha,
    });
  };

  onSubmit = () => {
    const { alphaText } = this.state;
    const { valid, alpha } = this.validateAlphaText(alphaText);
    if (!valid) return;

    this.setState({ stage: Stage.Solving }, () => this.sendRequest(alpha!));
  };

  /**
   * Called when the composition text is altered.
   */
  onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    const { valid } = this.validateAlphaText(value);

    this.setState({
      validAlphaText: valid,
      alphaText: value,
    });
  };

  render = () => {
    const { stage, T, alpha, validAlphaText, status, numSolutions } = this.state;

    const submitButton = (
      <Tooltip content='Find quasi-key tableaux'>
        <Button
          minimal
          icon='arrow-right'
          intent={Intent.PRIMARY}
          disabled={!validAlphaText}
          onClick={this.onSubmit}
        />
      </Tooltip>
    );

    return (
      <div>
        <FormGroup
          helperText=''
          label='composition'
          labelFor='text-input'
          labelInfo='(weak)'
        >
          <InputGroup
            placeholder='1, 2, 3, 4'
            onChange={this.onChange}
            intent={validAlphaText ? Intent.SUCCESS : Intent.DANGER}
            leftIcon='dot'
            rightElement={submitButton}
          />
        </FormGroup>
        {T && this.buildGrid(T.slice().reverse())}
        {alpha &&
          <div>
            <H5>Status: {status}</H5>
            <H5>Number of solutions: {numSolutions}</H5>
          </div>
        }
        {stage === Stage.Solving &&
          <ProgressBar
            className='sb-footer'
            value={1}
            stripes
          />
        }
      </div>
    );
  };
}

export default withStyles(styles)(QKTView);