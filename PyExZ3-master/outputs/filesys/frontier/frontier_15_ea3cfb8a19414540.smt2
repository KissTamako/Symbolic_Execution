(set-logic ALL)
; Constraint ID: ea3cfb8a19414540
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59557)) (False)
(assert (not (= x 59557)))

; Query: ((== x 59558)) (False)
(assert (not (not (= x 59558))))

(check-sat)
(get-model)
