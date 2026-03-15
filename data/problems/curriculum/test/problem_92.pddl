

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on-table b1)
(on b2 b9)
(on b3 b1)
(on-table b4)
(on b5 b7)
(on b6 b4)
(on b7 b8)
(on b8 b3)
(on-table b9)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b8)
(on b5 b9)
(on b6 b7)
(on b8 b5)
(on b9 b4))
)
)


