

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b12)
(ontable b3)
(on b4 b1)
(ontable b5)
(on b6 b9)
(on b7 b2)
(on b8 b6)
(on b9 b4)
(on b10 b8)
(ontable b11)
(on b12 b5)
(clear b3)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b9)
(on b2 b4)
(on b3 b11)
(on b4 b5)
(on b6 b12)
(on b9 b10)
(on b10 b2)
(on b11 b8)
(on b12 b3))
)
)


