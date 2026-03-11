

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b6)
(on b3 b2)
(on-table b4)
(on b5 b8)
(on b6 b4)
(on b7 b3)
(on b8 b1)
(on b9 b5)
(clear b7)
(clear b9)
)
(:goal
(and
(on b2 b5)
(on b3 b6)
(on b7 b2)
(on b8 b9)
(on b9 b7))
)
)


