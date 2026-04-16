(set-logic ALL)
; Constraint ID: 606d0a0dd148ba69
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60673)) (False)
(assert (not (= x 60673)))

; Query: ((== x 60674)) (False)
(assert (not (not (= x 60674))))

(check-sat)
(get-model)
