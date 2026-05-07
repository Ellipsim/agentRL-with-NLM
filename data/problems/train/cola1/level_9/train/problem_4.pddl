

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b6)
(on b3 b11)
(ontable b4)
(on b5 b3)
(ontable b6)
(ontable b7)
(on b8 b5)
(ontable b9)
(on b10 b2)
(on b11 b4)
(clear b1)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b3 b2)
(on b4 b11)
(on b6 b7)
(on b7 b5)
(on b9 b4)
(on b10 b9))
)
)


