

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on-table b3)
(on-table b4)
(on b5 b1)
(on b6 b8)
(on b7 b9)
(on b8 b5)
(on b9 b2)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b3)
(on b2 b8)
(on b4 b6)
(on b6 b5)
(on b7 b4)
(on b8 b1)
(on b9 b7))
)
)


