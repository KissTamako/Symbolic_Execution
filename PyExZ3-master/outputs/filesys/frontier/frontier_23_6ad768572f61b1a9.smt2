(set-logic ALL)
; Constraint ID: 6ad768572f61b1a9
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60394)) (False)
(assert (not (= x 60394)))

; Query: ((== x 60395)) (False)
(assert (not (not (= x 60395))))

(check-sat)
(get-model)
