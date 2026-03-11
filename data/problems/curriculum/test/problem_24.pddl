

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b9)
(on b3 b1)
(on-table b4)
(on b5 b10)
(on-table b6)
(on b7 b5)
(on-table b8)
(on b9 b7)
(on b10 b6)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b10)
(on b4 b7)
(on b5 b3)
(on b6 b8)
(on b8 b2)
(on b9 b5))
)
)


