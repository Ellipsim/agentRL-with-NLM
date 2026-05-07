

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b3)
(ontable b3)
(on b4 b10)
(on b5 b1)
(on b6 b4)
(ontable b7)
(ontable b8)
(on b9 b5)
(on b10 b2)
(clear b6)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b10)
(on b2 b8)
(on b4 b7)
(on b5 b4)
(on b6 b5)
(on b7 b2)
(on b8 b1)
(on b9 b6)
(on b10 b3))
)
)


