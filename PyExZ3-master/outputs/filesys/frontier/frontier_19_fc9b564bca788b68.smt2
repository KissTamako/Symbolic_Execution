(set-logic ALL)
; Constraint ID: fc9b564bca788b68
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59938)) (False)
(assert (not (= x 59938)))

; Query: ((== x 59939)) (False)
(assert (not (not (= x 59939))))

(check-sat)
(get-model)
