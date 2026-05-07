

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b6)
(on b3 b2)
(on b4 b5)
(ontable b5)
(ontable b6)
(on b7 b9)
(on b8 b4)
(ontable b9)
(on b10 b8)
(on b11 b10)
(on b12 b1)
(clear b3)
(clear b7)
(clear b12)
)
(:goal
(and
(on b1 b11)
(on b2 b7)
(on b3 b12)
(on b4 b10)
(on b5 b2)
(on b6 b9)
(on b8 b1)
(on b10 b6)
(on b11 b3))
)
)


