(set-logic ALL)
; Constraint ID: f6fb4997c2713998
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59554)) (False)
(assert (not (= x 59554)))

; Query: ((== x 59555)) (False)
(assert (not (not (= x 59555))))

(check-sat)
(get-model)
