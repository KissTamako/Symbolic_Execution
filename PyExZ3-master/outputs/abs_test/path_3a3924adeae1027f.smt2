(set-logic ALL)
; Executed Path ID: 3a3924adeae1027f
; Generated at: 2026-04-16 16:02:47
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const a Int)
(declare-const b Int)

; ((< a 0)) (True)
(assert (< a 0))
; ((== (abs a) b)) (True)
(assert (= (abs a) b))

(check-sat)
(get-model)
