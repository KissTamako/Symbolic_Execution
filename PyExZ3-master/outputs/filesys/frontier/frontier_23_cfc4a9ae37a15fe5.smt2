(set-logic ALL)
; Constraint ID: cfc4a9ae37a15fe5
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59419)) (False)
(assert (not (= x 59419)))

; Query: ((== x 59420)) (False)
(assert (not (not (= x 59420))))

(check-sat)
(get-model)
