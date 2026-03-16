

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b5)
(on b3 b4)
(on b4 b10)
(on b5 b3)
(ontable b6)
(on b7 b9)
(ontable b8)
(on b9 b1)
(on b10 b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b6)
(on b3 b7)
(on b4 b8)
(on b5 b2)
(on b6 b9)
(on b8 b10)
(on b9 b4)
(on b10 b3))
)
)


