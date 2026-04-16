(set-logic ALL)
; Path ID: 64d9cb8241553576
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60661)) (False)
(assert (not (not (= x 60661))))

(check-sat)
(get-model)
