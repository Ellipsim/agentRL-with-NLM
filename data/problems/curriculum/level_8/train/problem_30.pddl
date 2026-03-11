

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b8)
(on b3 b5)
(on b4 b6)
(on-table b5)
(on-table b6)
(on-table b7)
(on b8 b1)
(on b9 b4)
(clear b2)
(clear b3)
(clear b7)
)
(:goal
(and
(on b2 b4)
(on b3 b9)
(on b4 b7)
(on b8 b5))
)
)


