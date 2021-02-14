<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <div class="card" v-if="isStripeLoaded">
        <div class="info-area">
          <p class="name" v-text="product.name" />
          <p class="amount" v-text="'¥' + product.amount.toLocaleString() + '-'" />
          <client-only>
            <p class="stripe-area">
              <card
                :options="stripeOptions"
                :stripe="stripePK"
                class="stripe"
                @change="isEntered = $event.complete"
              />
            </p>
          </client-only>
          <div class="message" v-text="message" />
          <p class="button-area">
            <button
              class="button"
              :class="{ active: isEntered }"
              @click="pay"
              v-text="'PAYMENT'"
            />
          </p>
        </div>
        <div class="complete" :class="{ active: isComplete }">
          <p class="message" v-text="'Thank you!'" />
        </div>
      </div>

    </v-col>
  </v-row>
</template>

<script>
import { API } from 'aws-amplify'
import { Card, createToken } from 'vue-stripe-elements-plus'

export default {
  components: {
    Card,
  },
  data() {
    return {
      message: '',
      isEntered: false,
      isComplete: false,
      isStripeLoaded: false,
      stripeOptions: { hidePostalCode: true },
      stripePK: process.env.ENVVAL_STRIPE_PUBLIC_KEY,
      product: {
        name: 'SUPPORT PRODUCT',
        amount: 500,
      },
    }
  },
  methods: {
    async pay() {
      try {
        const tokenResult = await createToken()
        if (
          !tokenResult ||
          !tokenResult.token ||
          !tokenResult.token.id ||
          tokenResult.token.id === ''
        ) {
          return
        }
        const myInit = {
          headers: {},
          body: {
            'token': tokenResult.token.id,
            'amount': this.product.amount
          },
          response: true,
        };
        const response = await API.post(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/process', 
          myInit
        ).then(response => {
          this.isComplete = true
        }).catch(error => {
          console.log(error)
          this.message = error.message + 'が発生しました。'
        })
      } catch (error) {
        console.log(error)
        this.message = error.message + 'が発生しました。'
      }
    },

  },
  head() {
    return {
      script: [
        {
          hid: 'stripe',
          src: 'https://js.stripe.com/v3/',
          defer: true,
          callback: () => { this.isStripeLoaded = true } 
        }
      ]
    }
  },
}
</script>
<style lang="scss" scoped>
.container {
  padding: 24px;
  .title {
    text-align: center;
    font-size: 30px;
  }
  .card {
    border-radius: 8px;
    max-width: 480px;
    margin: 0 auto;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    position: relative;
    p {
      margin-top: 12px;
    }
    .info-area {
      background-color: #D5EBE7;
      padding: 16px;
      color: #064739;
      .name {
        font-size: 24px;
        text-align: center;
      }
      .amount {
        font-size: 24px;
        text-align: right;
      }
      .stripe-area {
        .stripe {
          border-bottom: dashed 2px #064739;
        }
      }
      .message {
        color: red;
        text-align: center;
      }
      .button-area {
        text-align: center;
        .button {
          cursor: pointer;
          background-color: #D5EBE7;
          color: #064739;
          border: 0;
          border-radius: 4px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
          padding: 4px 16px;
          font-size: 18px;
          &.active {
            background-color: #BBD347;
          }
        }
      }
    }
    .complete {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: rgba(255, 255, 255, 0.9);
      opacity: 0;
      z-index: -1;
      &.active {
        opacity: 1;
        z-index: 5;
      }
      .message {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: red;
        border: solid 2px red;
        border-radius: 25.5px;
        font-size: 36px;
        padding: 4px 24px;
        transform: rotate(-15deg);
      }
    }
  }
}
</style>