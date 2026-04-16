(set-logic ALL)
; Executed Path ID: 53b452852fb52d34
; Generated at: 2026-04-16 16:03:00
; Solver: Z3Wrapper
; Number of predicates: 7
; Has query: False

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)

; ((< a b)) (True)
(assert (< a b))
; ((< c d)) (True)
(assert (< c d))
; ((< b d)) (True)
(assert (< b d))
; ((< d a)) (False)
(assert (not (< d a)))
; ((< d b)) (False)
(assert (not (< d b)))
; ((< d c)) (False)
(assert (not (< d c)))
; ((< d d)) (False)
(assert (not (< d d)))

(check-sat)
(get-model)
