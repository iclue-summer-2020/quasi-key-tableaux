import React from 'react';
import {
  H3, ProgressBar, Dialog, InputGroup, Classes, Button, Colors, Intent, FormGroup, Tooltip, Icon,
} from '@blueprintjs/core';
import { SPACE } from '@blueprintjs/core/lib/esm/common/keys';

import Message, { TIMEOUT } from 'utils/Message';

import 'styles/QKTView.css';
import { withStyles, makeStyles, createStyles } from '@material-ui/styles';
import { Theme, WithStyles, Paper, Grid, Typography } from '@material-ui/core';

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
  validAlphaText: boolean | null;
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
      T: null,
      validAlphaText: null,
    };
  }

  componentDidMount = () => {

  };

  componentWillUnmount = () => {

  };

  doneSolving = () => {
    this.setState({
      stage: Stage.Finished,
    });
  };

  onNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  };

  onSubmit = (event: any) => {
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
                style={{ backgroundColor: 'gray' }}>
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

    const alpha = arr.map(Number.parseInt);
    if (alpha.length == 0) return notValid;
    if (alpha.some(x => x < 0)) return notValid;

    return { valid: true, alpha };
  };

  /**
   * Called when the composition text is altered.
   */
  onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    const { valid } = this.validateAlphaText(value);

    this.setState({
      validAlphaText: valid,
    });
  };

  render = () => {
    const { stage, T, alpha, validAlphaText } = this.state;

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
        {this.buildGrid(T || [[1, 1, 1], [2, 2, 2, 2]])}
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